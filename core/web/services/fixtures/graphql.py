import os
from web.services.core.request_builder.graphql import RequestBuilderGraphQL

from web.services.core.contracts.fixture import IFixtureWebService
from web.services.core.contracts.response import IResponse
from web.services.core.contracts.request import IWebServiceRequest
from web.services.core.clients.graphql import GraphQLClient
from web.services.core.config.webservice import AppConfigWSClient

from typing import TypeVar

TWebService = TypeVar("TWebService")


class BaseFixtureServiceGraphQL(IFixtureWebService[TWebService]):
    """
    A class implementing the IProtocolFixture interface for RESTful web services.

    This class provides methods for sending REST requests and initializing the necessary components
    for making those requests.
    """

    def __init__(self, config: AppConfigWSClient, gql_file, **kwargs):
        """
        Initializes the protocol fixture with the given configuration.

        Args:
            config: The AppConfigWSClient object containing the configuration for the web service client.
        """
        super(BaseFixtureServiceGraphQL, self)\
            .__init__(config=config, gql_file=gql_file, **kwargs)

        self.gql_file = gql_file
        self.base_path = kwargs.get('base_path', os.getcwd())

    def send_request(self, request: IWebServiceRequest, response_hook=dict, **kwargs) -> IResponse[TWebService]:
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

    def get_request_builder(self) -> RequestBuilderGraphQL:
        """
        Returns a request builder for constructing GraphQL web service requests.

        Returns:
            An instance of RequestBuilder for building GraphQL requests.
        """
        return RequestBuilderGraphQL(gql_file=self.gql_file, base_path=self.base_path)

    @property
    def client(self) -> GraphQLClient:
        """
        Returns the web client component of the protocol fixture.

        Return:
            The web client instance.
        """
        return self._client

    @property
    def request(self) -> RequestBuilderGraphQL:
        """
        Returns the request builder component of the protocol fixture.

        Return:
            The request builder instance.
        """
        if self._request is None:
            self._request = self.get_request_builder()
        return self._request
