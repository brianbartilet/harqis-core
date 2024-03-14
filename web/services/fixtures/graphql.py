from web.services.core.request_builder.graphql import RequestBuilderGraphQL

from web.services.core.contracts.fixture import IProtocolFixture
from web.services.core.contracts.request_builder import IWebRequestBuilder
from web.services.core.contracts.client import IWebClient
from web.services.core.contracts.response import IResponse
from web.services.core.contracts.request import IWebServiceRequest

from web.services.core.config.webservice import AppConfigWSClient

from typing import TypeVar
T = TypeVar("T")
V = TypeVar("V")


class BaseFixtureGraphQL(IProtocolFixture[T]):
    """
    A class implementing the IProtocolFixture interface for RESTful web services.

    This class provides methods for sending REST requests and initializing the necessary components
    for making those requests.
    """

    def __init__(self, config: AppConfigWSClient, **kwargs):
        """
        Initializes the protocol fixture with the given configuration.

        Args:
            config: The AppConfigWSClient object containing the configuration for the web service client.
        """
        super(BaseFixtureGraphQL, self).__init__(config=config)
        self.gql_file = kwargs.get('gql_file', None)
        self.base_path = kwargs.get('base_path', None)

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
        return RequestBuilderGraphQL(gql_file=self.gql_file, base_path=self.base_path)

    def initialize(self) -> (IWebRequestBuilder, IWebClient):
        """
        Initializes the REST protocol fixture and returns the request builder and web client components.

        Returns:
            A tuple containing the request builder and web client instances.
        """
        return self.request, self.client

