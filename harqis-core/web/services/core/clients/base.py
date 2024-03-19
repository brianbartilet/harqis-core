import requests
import urllib.parse as url_helper

from abc import ABC
from typing import TypeVar, Type, Dict

from utilities.logging.custom_logger import create_logger

from web.services.core.contracts.client import IWebClient
from web.services.core.contracts.request import IWebServiceRequest
from web.services.core.response import IResponse, Response


TResponseData = TypeVar('TResponseData')


class BaseWebClient(IWebClient, ABC):
    """
    A base class for a web client that implements the IWebClient interface.
    This class provides common functionality for sending HTTP requests and processing responses.
    """

    def __init__(self, base_url: str, *, response_encoding: str = "ascii", verify: bool = True,
                 use_session: bool = False, timeout: int = 5, **kwargs):
        """
        Initializes the BaseWebClient with the given configuration.

        Args:
            base_url: The base URL for the web service.
            response_encoding: The encoding to use for the response data. Defaults to 'ascii'.
            verify: Whether to verify SSL certificates. Defaults to True.
            use_session: Whether to use a session for making requests. Defaults to False.
            timeout: The timeout in seconds for the requests. Defaults to 5.
        """
        self.log = kwargs.get('logger', create_logger(self.__class__.__name__))

        self.session = requests.Session() if use_session else None
        self.base_url = base_url.rstrip('/')
        self.response_encoding = response_encoding
        self.verify = verify
        self.timeout = timeout
        self.cookies = {}
        self.proxies = {}
        self.response = None

    def set_request_timeout(self, timeout: int) -> None:
        """
        Sets the timeout for the requests.

        Args:
            timeout: The timeout in seconds.
        """
        self.timeout = timeout

    def set_session_cookies(self, cookies: Dict[str, str]) -> None:
        """
        Sets the cookies for the session if a session is being used.

        Args:
            cookies: A dictionary of cookies to be added to the session.
        """
        if self.session:
            self.session.cookies.update(cookies)

    def set_cookie_handler(self, cookies: Dict[str, str]) -> None:
        """
        Sets the cookie handler for the requests.

        Args:
            cookies: A dictionary of cookies to be sent with the requests.
        """
        self.cookies = cookies

    def set_proxies(self, proxies: Dict[str, str]) -> None:
        """
        Sets proxies for the requests.

        Args:
            proxies: A dictionary of proxies to be sent with the requests.
        """
        self.proxies = proxies

    def execute_request(self, r: IWebServiceRequest, response_hook: Type[TResponseData] = dict, **kwargs) -> IResponse[TResponseData]:
        """
        Executes a web service request and returns the response.

        Args:
            r: The web service request to be executed.
            response_hook: The type to deserialize the response data into.
            **kwargs: Additional keyword arguments to be passed to the request method.

        Return:
            An instance of IResponse containing the response data.
        """
        session = self.session or requests
        raw_url = self.__get_raw_url__(r.get_full_url())

        try:
            self.log.debug(f"\nREQUEST:\n"
                           f"\tmethod: {r.get_request_method().value.upper()}\n"
                           f"\turl: {raw_url}\n"
                           f"\tbody: {r.get_body()}\n")

            self.response = session.request(
                r.get_request_method().value,
                raw_url,
                cookies=self.cookies,
                verify=self.verify,
                timeout=self.timeout,
                params=r.get_query_strings(),
                headers=r.get_headers(),
                auth=r.get_authorization(),
                proxies=self.proxies,
                **r.get_body(),
                **kwargs
            )
        except Exception as e:
            self.log.error("Error sending %s request: %s", r.get_request_method().value, e)
            raise e

        return self.get_response(self.response, response_hook)

    def get_response(self, response: requests.Response, response_hook: Type[TResponseData]) -> IResponse[TResponseData]:
        """
        Processes the HTTP response and returns an IResponse instance.

        Args:
            response: The HTTP response received from the request.
            response_hook: The type to deserialize the response data into.

        Return:
            An instance of IResponse containing the processed response data.
        """
        self.response = Response(response_hook, data=None, response_encoding=self.response_encoding)
        self.response.set_status_code(response.status_code)
        self.response.set_headers(response.headers)
        self.response.set_raw_data(response.content)

        return self.response

    def get_errors(self) -> Type[TResponseData]:
        """
        Processes the HTTP response and returns an IResponse instance.

        Return:
            An instance of IResponse containing the processed response data.
        """
        raise NotImplementedError("This method must be implemented in a derived class.")

    def __get_raw_url__(self, url_path_without_base: str, param_str: str = "", strip_right: bool = False) -> str:
        """
        Constructs the full URL for the request.

        Args:
            url_path_without_base: The URL path without the base URL.
            param_str: Optional string to be appended to the URL path.
            strip_right: Whether to strip the rightmost slash from the URL.

        Return:
            The full URL as a string.
        """
        cleaned_url = url_path_without_base.strip("/")
        if param_str:
            cleaned_url += f"/{param_str}"

        full_url = url_helper.urljoin(self.base_url + "/", cleaned_url)
        return full_url.rstrip("/") if strip_right else full_url
