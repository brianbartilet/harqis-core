from abc import abstractmethod
from typing import TypeVar, Generic
from http import HTTPStatus

T = TypeVar("T")


class IApiResponse(Generic[T]):
    """
        This is a raw container that encapsulates whatever response object we will be getting, from which
        ever implementation we choose to do.
    """

    @property
    @abstractmethod
    def status_code(self) -> HTTPStatus:
        """
            HTTP Response Status Code
        :return:
        """
        ...

    @property
    @abstractmethod
    def headers(self):
        """
            HTTP Response Headers
        :return:
        """
        ...

    @property
    @abstractmethod
    def deserialized_data(self) -> T:
        """
            Returns a strongly typed object based on the inheriting class
        :return:
        """
        ...

    @property
    @abstractmethod
    def raw_data(self):
        """
            Returns the data as is, which is most likely a str
        :return:
        """
        ...

    @property
    @abstractmethod
    def raw_bytes(self) -> bytearray:
        """
            Returns an immutable sequence of integers
            bytes was chosen over bytearray as we should not be changing the values in the result
        :return:
        """
        ...
