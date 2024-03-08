from abc import abstractmethod, ABC
from typing import TypeVar, Type, Dict

from .response import IResponse
from .request import IWebServiceRequest

T = TypeVar("T")


class IWebClient(ABC):
    """
    Interface for a web client that can execute web service requests and handle responses.
    """

    @abstractmethod
    def execute_request(self, request_object: IWebServiceRequest, type_hook: Type[T]) -> IResponse[T]:
        """
        Execute a web service request and return the response.

        :param request_object: The request object to be executed.
        :param type_hook: The type to deserialize the response data into.
        :return: The response object.
        """
        ...

    @abstractmethod
    def set_cookie_handler(self, cookies: Dict[str, str]):
        """
        Set the cookie handler for the web client.

        :param cookies: A dictionary of cookies to be used by the web client.
        """
        ...

    @abstractmethod
    def set_session_cookies(self, cookies: Dict[str, str]):
        """
        Set the session cookies for the web client.

        :param cookies: A dictionary of session cookies to be used by the web client.
        """
        ...

    @abstractmethod
    def set_request_timeout(self, timeout: int):
        """
        Set the request timeout for the web client.

        :param timeout: The timeout in seconds.
        """
        ...

    @abstractmethod
    def get_response(self, response: IResponse, type_hook: Type[T]) -> IResponse[T]:
        """
        Get the response from the web client.

        :param response: The response object to be processed.
        :param type_hook: The type to deserialize the response data into.
        :return: The processed response object.
        """
        ...
