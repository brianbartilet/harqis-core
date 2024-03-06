from abc import abstractmethod
from typing import TypeVar, Type

from web.core.services.contracts.interfaces.iapi_response import IApiResponse

from web.core.services.contracts.interfaces.iapi_request import IApiRequest

T = TypeVar("T")


class IApiClient:
    config = None

    @abstractmethod
    def initialize(self):
        ...

    @abstractmethod
    def authorize(self):
        ...

    @abstractmethod
    def execute(self, request_object: IApiRequest, type_hook: Type[T]) -> IApiResponse[T]:
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

