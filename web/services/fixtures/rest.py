from web.services.core.request_builder.rest import RequestBuilderRest

from web.services.core.contracts.fixture import IProtocolFixture
from web.services.core.contracts.request_builder import IWebRequestBuilder
from web.services.core.contracts.client import IWebClient
from web.services.core.contracts.response import IResponse
from web.services.core.contracts.request import IWebServiceRequest


from typing import TypeVar
T = TypeVar("T")
V = TypeVar("V")


class BaseFixtureRest(IProtocolFixture[T]):
    """
    A class implementing the IProtocolFixture interface for RESTful web services.

    This class provides methods for sending REST requests and initializing the necessary components
    for making those requests.
    """

    def send_request(self, request: IWebServiceRequest, response_hook=dict, **kwargs) -> IResponse[T]:
        """
        Sends a RESTful web service request and returns the response.

        Args:
            request: The web service request to be sent.
            response_hook: The type to deserialize the response data into.
            **kwargs: Additional keyword arguments to be passed to the request.

        Returns:
            An instance of IResponse containing the response data.
        """
        return self._client.execute_request(request, response_hook, **kwargs)

    def get_request_builder(self) -> IWebRequestBuilder:
        """
        Returns a request builder for constructing RESTful web service requests.

        Returns:
            An instance of RequestBuilder for building RESTful requests.
        """
        return RequestBuilderRest()

    def initialize(self) -> (IWebRequestBuilder, IWebClient):
        """
        Initializes the REST protocol fixture and returns the request builder and web client components.

        Returns:
            A tuple containing the request builder and web client instances.
        """
        return self.request, self.client
