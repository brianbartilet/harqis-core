from abc import ABC
import requests
import urllib.parse as url_helper
from typing import TypeVar, Type, Dict

from utilities.logging.custom_logger import custom_logger

from web.services.core.contracts.client import IWebClient
from web.services.core.contracts.fixture import IWebServiceRequest
from web.services.core.response import IResponse, Response

T = TypeVar('T')


class BaseWebClient(IWebClient, ABC):
    """
    A base class for a web client that implements the IWebClient interface.
    This class provides common functionality for sending HTTP requests and processing responses.
    """

    def __init__(
        self,
        base_url: str,
        *,
        response_encoding: str = "ascii",
        verify_ssh: bool = True,
        use_session: bool = False,
        timeout: int = 5
    ):
        """
        Initializes the BaseWebClient with the given configuration.

        :param base_url: The base URL for the web service.
        :param response_encoding: The encoding to use for the response data. Defaults to 'ascii'.
        :param verify_ssh: Whether to verify SSL certificates. Defaults to True.
        :param use_session: Whether to use a session for making requests. Defaults to False.
        :param timeout: The timeout in seconds for the requests. Defaults to 5.
        """
        self.log = custom_logger('Generic Web Client')
        self.session = requests.Session() if use_session else None

        self.base_url = base_url.rstrip('/')
        self.response_encoding = response_encoding
        self.verify_ssh = verify_ssh
        self.timeout = timeout

        self.cookies = {}
        self.proxies = {}

    def set_request_timeout(self, timeout: int) -> None:
        """
        Sets the timeout for the requests.

        :param timeout: The timeout in seconds.
        """
        self.timeout = timeout

    def set_session_cookies(self, cookies: Dict[str, str]) -> None:
        """
        Sets the cookies for the session if a session is being used.

        :param cookies: A dictionary of cookies to be added to the session.
        """
        if self.session:
            self.session.cookies.update(cookies)

    def set_cookie_handler(self, cookies: Dict[str, str]) -> None:
        """
        Sets the cookie handler for the requests.

        :param cookies: A dictionary of cookies to be sent with the requests.
        """
        self.cookies = cookies

    def set_proxies(self, proxies: Dict[str, str]) -> None:
        """
        Sets the cookie handler for the requests.

        :param proxies: A dictionary of proxies to be sent with the requests.
        """
        self.proxies = proxies

    def execute_request(self, request: IWebServiceRequest, type_hook: Type[T], **kwargs) -> IResponse[T]:
        """
        Executes a web service request and returns the response.

        :param request: The web service request to be executed.
        :param type_hook: The type to deserialize the response data into.
        :param kwargs: Additional keyword arguments to be passed to the request method.
        :return: An instance of IResponse containing the response data.
        """
        session = self.session or requests
        raw_url = self.__get_raw_url__(request.get_full_url())

        try:
            response = session.request(
                request.get_request_method().value,
                raw_url,
                cookies=self.cookies,
                verify=self.verify_ssh,
                timeout=self.timeout,
                params=request.get_query_strings(),
                headers=request.get_headers(),
                auth=request.get_authorization(),
                proxies=self.proxies,
                **request.get_body(),
                **kwargs
            )
        except Exception as e:
            self.log.error("Error sending %s request: %s", request.get_request_method().value, e)
            raise e

        return self.get_response(response, type_hook)

    def get_response(self, response: requests.Response, type_hook: Type[T]) -> IResponse[T]:
        """
        Processes the HTTP response and returns an IResponse instance.

        :param response: The HTTP response received from the request.
        :param type_hook: The type to deserialize the response data into.
        :return: An instance of IResponse containing the processed response data.
        """
        result = Response(type_hook, data=None, response_encoding=self.response_encoding)
        result.set_status_code(response.status_code)
        result.set_headers(response.headers)
        result.set_raw_data(response.content)

        return result

    def __get_raw_url__(self, url_path_without_base: str, param_str: str = "", strip_right: bool = False) -> str:
        """
        Constructs the full URL for the request.

        :param url_path_without_base: The URL path without the base URL.
        :param param_str: Optional string to be appended to the URL path.
        :param strip_right: Whether to strip the rightmost slash from the URL.
        :return: The full URL as a string.
        """
        cleaned_url = url_path_without_base.strip("/")
        if param_str:
            cleaned_url += f"/{param_str}"

        full_url = url_helper.urljoin(self.base_url + "/", cleaned_url)
        return full_url.rstrip("/") if strip_right else full_url
