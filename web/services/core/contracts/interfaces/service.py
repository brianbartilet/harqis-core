from abc import abstractmethod
from typing import TypeVar, Generic

from .request_builder import IWebRequestBuilder
from .response import IResponse
from .request import IWebServiceRequest
from .client import IWebClient

T = TypeVar("T")


class IWebService(Generic[T]):

    @abstractmethod
    def send_get_request(self, request: IWebServiceRequest) -> IResponse[T]:
        ...

    @abstractmethod
    def send_post_request(self, request: IWebServiceRequest) -> IResponse[T]:
        ...

    @abstractmethod
    def send_delete_request(self, request: IWebServiceRequest) -> IResponse[T]:
        ...

    @abstractmethod
    def send_put_request(self, request: IWebServiceRequest) -> IResponse[T]:
        ...

    @abstractmethod
    def send_patch_request(self, request: IWebServiceRequest) -> IResponse[T]:
        ...

    @abstractmethod
    def get_request_builder(self) -> IWebRequestBuilder:
        ...

    @abstractmethod
    def initialize(self) -> (IWebRequestBuilder, IWebClient):
        ...

    @abstractmethod
    def set_session_data(self, **kwargs):
        ...