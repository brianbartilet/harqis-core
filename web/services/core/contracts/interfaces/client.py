from abc import abstractmethod, ABC
from typing import TypeVar, Type

from .response import IResponse
from .request import IWebServiceRequest

T = TypeVar("T")


class IWebClient(ABC):
    config = None

    @abstractmethod
    def initialize(self):
        ...

    @abstractmethod
    def authorize(self):
        ...

    @abstractmethod
    def execute(self, request_object: IWebServiceRequest, type_hook: Type[T]) -> IResponse[T]:
        ...

    @abstractmethod
    def set_cookie_handler(self, cookies: dict):
        ...

    @abstractmethod
    def set_session_cookies(self, timeout: int):
        ...

    @abstractmethod
    def set_default_headers(self, headers: dict):
        ...

    @abstractmethod
    def set_request_timeout(self, timeout: int):
        ...

