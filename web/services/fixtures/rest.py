from web.services.core.request_builder.rest import RequestBuilderRest

from web.services.core.clients.rest import RestClient

from web.services.core.contracts.fixture import IFixtureWebService
from web.services.core.contracts.response import IResponse
from web.services.core.contracts.request import IWebServiceRequest

from web.services.core.config.webservice import AppConfigWSClient

from typing import TypeVar
T = TypeVar("T")
V = TypeVar("V")


class BaseFixtureServiceRest(IFixtureWebService[T]):
    """
    A class implementing the IProtocolFixture interface for RESTful web services.

    This class provides methods for sending REST requests and initializing the necessary components
    for making those requests.
    """

    def __init__(self, config: AppConfigWSClient, **kwargs):
        super(BaseFixtureServiceRest, self).__init__(config=config)

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
        return super().send_request(request, response_hook, **kwargs)

    def get_request_builder(self) -> RequestBuilderRest:
        """
        Returns a request builder for constructing RESTful web service requests.

        Returns:
            An instance of RequestBuilder for building RESTful requests.
        """
        return RequestBuilderRest()

    @property
    def client(self) -> RestClient:
        """
        Returns the web client component of the protocol fixture.

        Return:
            The web client instance.
        """
        return self._client

    @property
    def request(self) -> RequestBuilderRest:
        """
        Returns the request builder component of the protocol fixture.

        Return:
            The request builder instance.
        """
        if self._request is None:
            self._request = self.get_request_builder()
        return self._request
