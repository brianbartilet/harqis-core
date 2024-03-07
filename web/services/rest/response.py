from http import HTTPStatus
from typing import TypeVar, Type

from web.services.core.contracts.interfaces.response import IResponse
from utilities.json_util import JsonUtil
from utilities.custom_logger import custom_logger

T = TypeVar("T")


class Response(IResponse[T]):

    def __init__(self, type_hook: Type[T], data, response_encoding="ascii"):
        self.__type_hook = type_hook
        self.__data = data
        self.__encoding = response_encoding
        self.__headers = None
        self.__status_code = None
        self.log = custom_logger()

    # region Unexposed methods, unless explicitly created

    def set_header(self, header):
        if header is None:
            raise ValueError("Headers can never be null")
        self.__headers = header

    def set_raw_data(self, data):
        self.__data = data

    def set_status_code(self, status_code: int):
        self.__status_code = HTTPStatus(status_code)

    # endregion

    # region Interface implementation

    @property
    def json_data(self) -> T:
        #  switch to application type
        return JsonUtil.deserialize(self.__data.decode(self.__encoding), self.__type_hook)

    @property
    def raw_bytes(self) -> bytearray:
        if self.__data is None:
            return bytearray()

        if isinstance(self.__data, str):
            return bytearray(self.__data, self.__encoding)

        return bytearray(self.__data)

    @property
    def raw_data(self):
        return self.__data

    # endregion

    @property
    def status_code(self) -> HTTPStatus:
        if self.__status_code is None:
            raise ValueError("No status code found for this response. Could be a connection issue")
        return self.__status_code

    @property
    def headers(self):
        return self.__headers

    # endregion
