from abc import abstractmethod
from typing import TypeVar, Generic, Dict
from http import HTTPStatus

TResponse = TypeVar("TResponse")


class IResponse(Generic[TResponse]):
    """
    A generic container for encapsulating HTTP responses.
    """

    @property
    @abstractmethod
    def status_code(self) -> HTTPStatus:
        """
        Returns the HTTP response status code.
        """
        ...

    @property
    @abstractmethod
    def headers(self) -> Dict[str, str]:
        """
        Returns the HTTP response headers.
        """
        ...

    @property
    @abstractmethod
    def data(self) -> TResponse:
        """
        Returns a strongly typed object based on the response data.
        """
        ...

    @property
    @abstractmethod
    def raw_data(self) -> str:
        """
        Returns the response data as a string.
        """
        ...

    @property
    @abstractmethod
    def raw_bytes(self) -> bytes:
        """
        Returns the response data as an immutable sequence of bytes.
        """
        ...
