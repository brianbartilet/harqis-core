import functools
import time

from abc import ABC
from http import HTTPStatus
from typing import TypeVar, Type, Optional
from requests.structures import CaseInsensitiveDict

from web.services.core.contracts.response import IResponse
from utilities.json_util import JsonUtil
from utilities.logging.custom_logger import custom_logger
from utilities.data_helpers.objects import ObjectUtilities

from .dto import BaseDto

T = TypeVar("T")

def deserialized(type_hook: Type[T] = BaseDto, child: str = None, wait=None):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(self, *args, **kwargs):
            log = custom_logger('Deserialize decorator for response')
            self.initialize()
            self.response_type = type_hook

            if wait is not None:
                time.sleep(wait)

            response_instance = func(self, *args, **kwargs)

            if self._config.return_data_only:
                try:
                    if child is not None:
                        if isinstance(type_hook(), dict):
                            return ObjectUtilities.convert_object_keys_to_snake_case(response_instance.json_data[child])
                        else:
                            return ObjectUtilities.convert_object_keys_to_snake_case(eval("response.deserialized_data." + child))
                    else:
                        return ObjectUtilities.convert_object_keys_to_snake_case(response_instance.json_data)

                except Exception as e:
                    log.warning("Cannot access deserialized data. Returning full response. ERROR: {0}".format(e))
                    return response_instance

            else:
                return response_instance

        return wrapper

    return decorator

class Response(IResponse[T], ABC):

    def __init__(self, type_hook: Type[T], data: Optional[bytes], response_encoding: str = "ascii"):
        self.log = custom_logger("Web Response")

        self.__type_hook = type_hook
        self.__data = data
        self.__encoding = response_encoding
        self.__headers = CaseInsensitiveDict()
        self.__status_code: Optional[HTTPStatus] = None

    def set_headers(self, headers: CaseInsensitiveDict[str]):
        if headers is None:
            raise ValueError("Headers can never be null")
        self.__headers = headers

    def set_raw_data(self, data: bytes):
        self.__data = data

    def set_status_code(self, status_code: int):
        self.__status_code = HTTPStatus(status_code)

    @property
    def json_data(self) -> T:
        try:
            return JsonUtil.deserialize(self.__data.decode(self.__encoding), self.__type_hook)
        except Exception as e:
            self.log.error(f"Error deserializing JSON data: {e}")
            raise

    @property
    def raw_bytes(self) -> bytes:
        if self.__data is None:
            return bytes()

        if isinstance(self.__data, str):
            return self.__data.encode(self.__encoding)

        return bytes(self.__data)

    @property
    def raw_data(self) -> Optional[bytes]:
        return self.__data

    @property
    def status_code(self) -> HTTPStatus:
        if self.__status_code is None:
            raise ValueError("No status code found for this response. Could be a connection issue")
        return self.__status_code

    @property
    def headers(self) -> CaseInsensitiveDict[str]:
        return self.__headers
