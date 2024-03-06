from abc import abstractmethod
from typing import TypeVar, Generic

from web.core.services.contracts.interfaces.iapi_request_builder import IApiRequestBuilder
from web.core.services.contracts.interfaces.iapi_response import IApiResponse

from web.core.services.contracts.interfaces.iapi_request import IApiRequest
from web.core.services.contracts.interfaces.iapi_client import IApiClient

T = TypeVar("T")


class IApiService(Generic[T]):

    @abstractmethod
    def send_get_request(self, request: IApiRequest) -> IApiResponse[T]:
        ...

    @abstractmethod
    def send_post_request(self, request: IApiRequest) -> IApiResponse[T]:
        ...

    @abstractmethod
    def send_delete_request(self, request: IApiRequest) -> IApiResponse[T]:
        ...

    @abstractmethod
    def send_put_request(self, request: IApiRequest) -> IApiResponse[T]:
        ...

    @abstractmethod
    def send_patch_request(self, request: IApiRequest) -> IApiResponse[T]:
        ...

    @abstractmethod
    def get_request_builder(self) -> IApiRequestBuilder:
        ...

    @abstractmethod
    def initialize(self) -> (IApiRequestBuilder, IApiClient):
        ...

    @abstractmethod
    def set_session_data(self, **kwargs):
        ...