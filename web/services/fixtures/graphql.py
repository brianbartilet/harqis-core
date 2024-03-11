from web.services.core.contracts import *
from web.services.core.request_builder import RequestBuilder

from typing import TypeVar
T = TypeVar("T")
V = TypeVar("V")

class FixtureGraphQL(IProtocolFixture[T]):
    """
    A class implementing the IProtocolFixture interface for RESTful web services.

    This class provides methods for sending REST requests and initializing the necessary components
    for making those requests.
    """

    def send_request(self, r: IWebServiceRequest, **kwargs) -> IResponse[T]:
        """
        Sends a RESTful web service request and returns the response.

        Args:
            r: The web service request to be sent.
            **kwargs: Additional keyword arguments to be passed to the request.

        Returns:
            An instance of IResponse containing the response data.
        """
        return self._client.execute_request(r, self.response_type, **kwargs)

    def get_request_builder(self) -> IWebRequestBuilder:
        """
        Returns a request builder for constructing RESTful web service requests.

        Returns:
            An instance of RequestBuilder for building RESTful requests.
        """
        return RequestBuilder()

    def initialize(self) -> (IWebRequestBuilder, IWebClient):
        """
        Initializes the REST protocol fixture and returns the request builder and web client components.

        Returns:
            A tuple containing the request builder and web client instances.
        """
        return self.request, self.client
