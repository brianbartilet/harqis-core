import functools
import time

from typing import Any, get_origin, get_args, List
from typing import TypeVar, Type, Optional
from dataclasses import is_dataclass

from core.web.services.core.contracts.response import IResponse
from core.web.services.core.json import  JsonObject
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

    return decorator