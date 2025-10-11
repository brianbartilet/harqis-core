import functools
import time

from typing import Any, get_origin, get_args, List
from abc import ABC
from http import HTTPStatus
from typing import TypeVar, Type, Optional
from requests.structures import CaseInsensitiveDict
from dataclasses import is_dataclass

from core.web.services.core.contracts.response import IResponse
from core.web.services.core.json import JsonUtility, JsonObject
from core.utilities.data.strings import convert_object_keys_to_snake
from core.utilities.logging.custom_logger import create_logger

TResponse = TypeVar("TResponse")
TTypeHook = TypeVar("TTypeHook")


def deserialized(type_hook: Type[TTypeHook], child: str = None, wait=None):
    """
    Deserializes a response into the specified DTO type or list[DTO] when
    self._config.return_data_only is True, Otherwise returns the response instance.

    - type_hook can be:
        * A DTO class (e.g., DtoAccountProperties) -> returns that DTO instance
        * A typing list of DTOs (e.g., list[DtoAccountProperties]) -> returns list[DTO]
        * dict -> returns a plain dict (with snake_case keys)
    - child: optional key/attribute to select from response.data BEFORE conversion
    - wait: optional sleep (seconds) before performing the call
    """
    def _is_list_type(tp: Any) -> bool:
        return get_origin(tp) in (list, List)

    def _list_item_type(tp: Any) -> Optional[Type[Any]]:
        if not _is_list_type(tp):
            return None
        args = get_args(tp)
        return args[0] if args else None

    def _to_dict(obj: Any) -> Any:
        # Convert JsonObject -> dict; pass through dicts/lists; otherwise return as-is
        if isinstance(obj, JsonObject):
            return dict(obj)
        return obj

    def _access_child(container: Any, key: Optional[str]) -> Any:
        if not key:
            return container
        # Try attribute access first (for JsonObject / typed objects), then dict key
        if hasattr(container, key):
            return getattr(container, key)
        if isinstance(container, dict):
            return container[key]
        raise KeyError(f"Child '{key}' not found in response data.")

    def _construct_one(d: Any, cls: Type[Any]) -> Any:
        """
        Build a single DTO instance from dict-like data,
        supporting dataclasses, .from_dict(), or **kwargs constructors.
        """
        d = _to_dict(d)
        if isinstance(d, JsonObject):
            d = dict(d)
        if not isinstance(d, dict):
            # If the API already returns a proper instance, just return it
            if isinstance(d, cls):
                return d
            raise TypeError(f"Cannot construct {cls.__name__} from non-dict: {type(d)}")

        if is_dataclass(cls):
            return cls(**d)
        if hasattr(cls, "from_dict") and callable(getattr(cls, "from_dict")):
            return cls.from_dict(d)
        return cls(**d)

    def _coerce_to_type(value: Any, hook: Type[Any]) -> Any:
        """
        Coerce `value` into `hook`, supporting:
        - dict -> dict (snake_case keys)
        - DTO class
        - list[DTO]
        """
        # If the hook is dict-like request, just return snake-cased dict/list
        if hook is dict:
            return convert_object_keys_to_snake(_to_dict(value))

        # list[DTO]?
        if _is_list_type(hook):
            elem_type = _list_item_type(hook)
            if elem_type is None:
                raise TypeError("List type_hook must specify an item type, e.g. list[MyDto]")
            # Ensure we have a list to map over
            seq = value
            if isinstance(seq, JsonObject):
                seq = list(seq)  # unlikely, but for safety
            if not isinstance(seq, list):
                raise TypeError(f"Expected list payload for {hook}, got {type(seq)}")
            return [ _construct_one(item, elem_type) for item in seq ]

        # Single DTO class
        return _construct_one(value, hook)

    def decorator(func):
        @functools.wraps(func)
        def wrapper(self, *args, **kwargs):
            log = create_logger('JSON Deserialization decorator for response')

            if wait is not None:
                time.sleep(wait)

            response_instance: IResponse = func(self, *args, **kwargs)

            # If user wants the deserialized payload only, produce it
            if getattr(self, "_config", None) and getattr(self._config, "return_data_only", False):
                try:
                    data = response_instance.data  # already deserialized to Python via Response.data
                    # pick child if requested
                    data = _access_child(data, child)

                    # Now coerce into the desired type (DTO or list[DTO] or dict)
                    coerced = _coerce_to_type(data, type_hook)

                    # Finally, snake-case keys if it’s dicts (deeply) to be consistent with your original intent
                    if type_hook is dict:
                        return convert_object_keys_to_snake(coerced)
                    # If coerced is a list of dicts (rare if DTOs are dataclasses), you can optionally normalize here
                    return coerced

                except Exception as e:
                    log.warning(f"Cannot deserialize into requested type. Returning full response. ERROR: {e}")
                    return response_instance

            # Otherwise, return the response wrapper (raw mode)
            return response_instance

        return wrapper


class Response(IResponse[TResponse], ABC):
    """
    A class representing a web service response.
    """

    def __init__(self, type_hook: Type[TTypeHook], data: Optional[bytes], response_encoding: str = "ascii", **kwargs):
        """
        Initializes the Response object.

        Args:
            type_hook: The type to deserialize the response data into.
            data: The raw response data.
            response_encoding: The encoding of the response data.
        """
        self.log = kwargs.get('logger', create_logger(self.__class__.__name__))
        self.__data_key = kwargs.get('data_key', None)

        self.__type_hook = type_hook
        self.__data = data
        self.__encoding = response_encoding
        self.__headers = CaseInsensitiveDict()
        self.__status_code: Optional[HTTPStatus] = None

    def set_headers(self, headers: CaseInsensitiveDict[str]):
        """
        Sets the headers of the response.

        Args:
            headers: The headers to set.
        """
        if headers is None:
            raise ValueError("Headers can never be null")
        self.__headers = headers

    def set_raw_data(self, data: bytes):
        """
        Sets the raw data of the response.

        Args:
            data: The raw data to set.
        """
        self.__data = data

    def set_status_code(self, status_code: int):
        """
        Sets the status code of the response.

        Args:
            status_code: The status code to set.
        """
        self.__status_code = HTTPStatus(status_code)

    @property
    def data(self) -> TResponse:
        """
        Returns the deserialized JSON data of the response.

        Returns:
            The deserialized JSON data.
        """
        try:
            data = JsonUtility.deserialize(self.__data.decode(self.__encoding), self.__type_hook)
            if self.__data_key is not None:
                if isinstance(data, JsonObject):
                    return eval(f"data.{self.__data_key}")
                else:
                    return data[self.__data_key]
            return data

        except Exception as e:
            self.log.error(f"Error deserializing JSON data: {e}")
            raise

    @property
    def raw_bytes(self) -> bytes:
        """
        Returns the raw bytes of the response.

        Returns:
            The raw bytes of the response.
        """
        if self.__data is None:
            return bytes()

        if isinstance(self.__data, str):
            return self.__data.encode(self.__encoding)

        return bytes(self.__data)

    @property
    def raw_data(self) -> Optional[bytes]:
        """
        Returns the raw data of the response.

        Returns:
            The raw data of the response.
        """
        return self.__data

    @property
    def status_code(self) -> HTTPStatus:
        """
        Returns the status code of the response.

        Returns:
            The status code of the response.
        """
        if self.__status_code is None:
            raise ValueError("No status code found for this response. Could be a connection issue")
        return self.__status_code

    @property
    def headers(self) -> CaseInsensitiveDict[str]:
        """
        Returns the headers of the response.

        Returns:
            The headers of the response.
        """
        return self.__headers
