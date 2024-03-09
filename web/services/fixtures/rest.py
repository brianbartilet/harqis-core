from web.services.core.contracts import *
from web.services.core.request_builder import RequestBuilder

from typing import TypeVar
T = TypeVar("T")
V = TypeVar("V")

class RestProtocolFixture(IProtocolFixture[T]):

    def send_request(self, r: IWebServiceRequest, **kwargs) -> IResponse[T]:
        return self._client.execute_request(r, self.response_type, **kwargs)

    def get_request_builder(self) -> IWebRequestBuilder:
        return RequestBuilder()

    def initialize(self) -> (IWebRequestBuilder, IWebClient):
        return self.request, self.client
