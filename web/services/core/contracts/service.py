from abc import abstractmethod
from typing import TypeVar, Generic

from .request_builder import IWebRequestBuilder
from .response import IResponse
from .request import IWebServiceRequest
from .client import IWebClient

T = TypeVar("T")


class IWebService(Generic[T]):

    @abstractmethod
    def initialize(self) -> (IWebRequestBuilder, IWebClient):
        ...

    @abstractmethod
    def get_request_builder(self) -> IWebRequestBuilder:
        ...

    @abstractmethod
    def send_request(self, r: IWebServiceRequest, **kwargs) -> IResponse[T]:
        ...

    @abstractmethod
    def set_session_data(self, **kwargs):
        ...
