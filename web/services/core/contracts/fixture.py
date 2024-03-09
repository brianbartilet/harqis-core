from abc import abstractmethod
from typing import TypeVar, Generic, Type
T = TypeVar("T")

from .request_builder import IWebRequestBuilder
from .response import IResponse
from .request import IWebServiceRequest
from .client import IWebClient

from web.services.core.constants.service_client_type import WSClientName
from web.services.core.config.webservice import BaseAppConfigWSClient
from web.services.core.clients import *

from utilities.asserts.helper import LoggedAssertHelper

class WSClientClass:
    """
    A class that maps web service client names to their corresponding client classes.

    This class provides a way to dynamically select the appropriate client class based on
    the web service client name. It is used to instantiate the correct client for making
    web service requests.

    Attributes:
        map (dict): A dictionary mapping web service client names to their corresponding
                    client classes. The keys are values from the WSClientName enum, and
                    the values are the client classes.
    """
    map = {
        str(WSClientName.GENERIC): RestClient,
        str(WSClientName.CURL): RestClient,
        str(WSClientName.SOAP): RestClient,
        str(WSClientName.REST): RestClient,
        str(WSClientName.GRAPHQL): GraphQLClient,
        str(WSClientName.GRPC): GrpcClient
    }


class IProtocolFixture(Generic[T]):
    """
    An interface for a testing fixture that aggregates components for building and sending web requests.

    This interface defines methods for initializing the fixture, obtaining a request builder, and sending requests.
    It is designed to be used in testing scenarios where different parts of a web service interaction need to be
    set up, executed, and observed.

    The fixture uses a generic type T to represent the type of the response data expected from the web service.
    """
    response_type: Type[T]

    @abstractmethod
    def initialize(self) -> (IWebRequestBuilder, IWebClient):
        """
        Initializes the testing fixture and returns the request builder and web client components.

        :return: A tuple containing the request builder and web client instances.
        """
        ...

    @abstractmethod
    def get_request_builder(self) -> IWebRequestBuilder:
        """
        Returns the request builder component of the testing fixture.

        The request builder is used to construct web service requests in a fluent and flexible manner.

        :return: An instance of a class that implements the IWebRequestBuilder interface.
        """
        ...

    @abstractmethod
    def send_request(self, request: IWebServiceRequest, **kwargs) -> IResponse[T]:
        """
        Sends a web service request using the web client component and returns the response.

        :param request: The web service request to be sent.
        :param kwargs: Optional keyword arguments that may be required for sending the request.
        :return: An instance of a class that implements the IResponse interface, containing the response data.
        """
        ...

    def __init__(self, config: BaseAppConfigWSClient):
        self._config = config
        self._client = WSClientClass.map[config.client](**config.parameters)
        self._request = None

    @property
    def client(self) -> IWebClient:
        """Get the web client."""
        return self._client

    @property
    def request(self) -> IWebRequestBuilder:
        """Get the request instance from builder."""
        if self._request is None:
            self._request = self.get_request_builder()
        return self._request

    @property
    def app_data(self) -> dict:
        """Get the parameters."""
        return self._config.app_data

    @property
    def verify(self) -> LoggedAssertHelper:
        """Get the logged assert helper."""
        return LoggedAssertHelper()
