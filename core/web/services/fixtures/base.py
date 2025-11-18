from typing import TypeVar, Generic, Type

from core.web.services.core.contracts.request_builder import IWebRequestBuilder
from core.web.services.core.contracts.response import IResponse
from core.web.services.core.contracts.request import IWebServiceRequest
from core.web.services.core.contracts.client import IWebClient

from core.web.services.core.constants.service_client_type import WebService
from core.web.services.core.config.webservice import AppConfigWSClient
from core.web.services.core.clients.rest import RestClient
from core.web.services.core.clients.graphql import GraphQLClient
from core.web.services.core.clients.grpc import GrpcClient

from core.utilities.asserts.helper import LoggedAssertHelper

TFixture = TypeVar("TFixture")
TResponse = TypeVar("TResponse")


class WSClientClass:
    """
    A class that maps web service client names to their corresponding client classes.

    Attributes:
        map (dict): A dictionary mapping web service client names to their corresponding
                    client classes. The keys are values from the WSClientName enum, and
                    the values are the client classes.
    """
    map = {
        WebService.GENERIC.value: RestClient,
        WebService.CURL.value: RestClient,
        WebService.SOAP.value: RestClient,
        WebService.REST.value: RestClient,
        WebService.GRAPHQL.value: GraphQLClient,
        WebService.GRPC.value: GrpcClient
    }


class IFixtureWebService(Generic[TFixture]):
    """
    An interface for a testing fixture that aggregates components for building and sending web requests.

    This interface defines methods for initializing the fixture, obtaining a request builder, and sending requests.
    It is designed to be used in testing scenarios where different parts of a web service interaction need to be
    set up, executed, and observed.

    The fixture uses a generic type T to represent the type of the response data expected from the web service.
    """

    def __init__(self, config: AppConfigWSClient, **kwargs):
        """
        Initializes the protocol fixture with the given configuration.

        Args:
            config: The AppConfigWSClient object containing the configuration for the web service client.
        """
        self._config = config
        # allow custom client to be processed e.g. google python client
        self._client = kwargs.get('client', WSClientClass.map[config.client](**config.parameters))
        self._request = None

        self.kwargs = kwargs

    def get_request_builder(self) -> IWebRequestBuilder:
        """
        Returns the request builder component of the testing fixture.

        The request builder is used to construct web service requests in a fluent and flexible manner.

        Return:
            An instance of a class that implements the IWebRequestBuilder interface.
        """
        ...

    def send_request(self, request: IWebServiceRequest, response_hook: Type[TResponse] = dict,
                     **kwargs) -> IResponse[TFixture]:
        """
        Sends a web service request using the web client component and returns the response.

        Args:
            request: The web service request to be sent.
            response_hook: The type to deserialize the response data into.
            kwargs: Optional keyword arguments that may be required for sending the request.

        Return:
            An instance of a class that implements the IResponse interface, containing the response data.
        """
        return self._client.execute_request(request, response_hook, **kwargs)

    @property
    def config(self) -> AppConfigWSClient:
        """
        Returns the web client component of the protocol fixture.

        Return:
            The web client instance.
        """
        return self._config

    @property
    def client(self) -> IWebClient:
        """
        Returns the web client component of the protocol fixture.

        Return:
            The web client instance.
        """
        return self._client

    @property
    def request(self) -> IWebRequestBuilder:
        """
        Returns the request builder component of the protocol fixture.

        Return:
            The request builder instance.
        """
        if self._request is None:
            self._request = self.get_request_builder()
        return self._request

    @property
    def verify(self) -> LoggedAssertHelper:
        """
        Returns the logged assert helper for performing assertions.

        Return:
            An instance of LoggedAssertHelper.
        """
        return LoggedAssertHelper()
