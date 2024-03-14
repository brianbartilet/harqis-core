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
    def execute_request(self, request: IWebServiceRequest, response_hook: Type[T] = dict, **kwargs) -> IResponse[T]:
        """
        Execute a web service request and return the response.

        Args:
            request: The request object to be executed.
            response_hook: The type to deserialize the response data into.

        Return:
            The response object.
        """
        ...

    @abstractmethod
    def set_cookie_handler(self, cookies: Dict[str, str]):
        """
        Set the cookie handler for the web client.

        Args:
            cookies: A dictionary of cookies to be used by the web client.
        """
        ...

    @abstractmethod
    def set_session_cookies(self, cookies: Dict[str, str]):
        """
        Set the session cookies for the web client.

        Args:
            cookies: A dictionary of session cookies to be used by the web client.
        """
        ...

    @abstractmethod
    def set_proxies(self, proxies: Dict[str, str]):
        """
        Set proxies for the web client.

        Args:
            proxies: A dictionary of URI proxies to be passed to the web client.
        """
        ...

    @abstractmethod
    def set_request_timeout(self, timeout: int):
        """
        Set the request timeout for the web client.

        Args:
            timeout: The timeout in seconds.
        """
        ...

    @abstractmethod
    def get_response(self, response: IResponse, type_hook: Type[T]) -> IResponse[T]:
        """
        Get the response from the web client.

        Args:
            response: The response object to be processed.
            type_hook: The type to deserialize the response data into.

        Return:
            The processed response object.
        """
        ...

    @abstractmethod
    def get_errors(self) -> Type[T]:
        """
        Get the errors from the web client.

        Return:
            The errors from the web client.
        """
        ...
