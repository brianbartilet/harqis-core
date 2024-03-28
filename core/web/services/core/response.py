import functools
import time

from abc import ABC
from http import HTTPStatus
from typing import TypeVar, Type, Optional
from requests.structures import CaseInsensitiveDict

from core.web.services.core.contracts.response import IResponse
from core.web.services.core.json import JsonUtility, JsonObject
from core.utilities.data.objects import convert_object_keys_to_snake
from core.utilities.logging.custom_logger import create_logger

TResponse = TypeVar("TResponse")
TTypeHook = TypeVar("TTypeHook")


def deserialized(type_hook: Type[TTypeHook], child: str = None, wait=None):
    """
    ***DEPRECATED***
    A decorator that deserializes the response data into the specified type.

    Args:
        type_hook: The type to deserialize the response data into.
        child: The child attribute of the response data to be deserialized.
        wait: The time to wait before deserializing the response.

    Returns:
        The deserialized response data.
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(self, *args, **kwargs):
            log = create_logger('JSON Deserialization decorator for response')
            #self.initialize()

            if wait is not None:
                time.sleep(wait)

            response_instance = func(self, *args, **kwargs)

            if self._config.return_data_only:
                try:
                    if child is not None:
                        if isinstance(type_hook(), dict):
                            return convert_object_keys_to_snake(response_instance.data[child])
                        else:
                            return convert_object_keys_to_snake(eval("response.deserialized_data." + child))
                    else:
                        return convert_object_keys_to_snake(response_instance.data)

                except Exception as e:
                    log.warning(f"Cannot access deserialized data. Returning full response. ERROR: {e}")
                    return response_instance

            else:
                return response_instance

        return wrapper

    return decorator


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
