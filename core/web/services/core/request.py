from abc import ABC
from typing import Optional, Dict

from requests.structures import CaseInsensitiveDict
from core.web.services.core.constants.http_methods import HttpMethod
from core.web.services.core.contracts.request import IWebServiceRequest
from core.utilities.logging.custom_logger import create_logger


class Request(IWebServiceRequest, ABC):
    """
    Represents a web service request.

    Attributes:
        body (Dict[str, str]): The request body as a dictionary.
        full_uri (str): The full URI of the request.
        request_type (HttpMethod): The HTTP method of the request.
        headers (Dict[str, str]): The request headers as a dictionary.
        query_string (Dict[str, str]): The query string parameters as a dictionary.
        auth (Optional[Dict[str, str]]): The authentication credentials, if any.
        __strip_right_url (bool): Flag to indicate whether to strip the right side of the URL.

    """

    def __init__(self, **kwargs):
        """
        Initializes a new instance of the Request class.

        Args:
            **kwargs: Optional keyword arguments to set the request properties.
        """
        self.log = kwargs.get('logger', create_logger(self.__class__.__name__))

        self.body: Dict[str, str] = kwargs.get('body', {})
        self.full_uri: str = kwargs.get('full_uri', "")
        self.request_type: HttpMethod = kwargs.get('request_type', HttpMethod.GET)
        self.headers: Dict[str, str] = kwargs.get('headers', {})
        self.query_string: Dict[str, str] = kwargs.get('query_string', {})
        self.auth: Optional[Dict[str, str]] = kwargs.get('auth', None)

        self.__strip_right_url: bool = True

    def get_query_strings(self) -> Dict[str, str]:
        """Gets the query string parameters."""
        return self.query_string

    def set_query_string(self, q_strings: Dict[str, str]):
        """Sets the query string parameters."""
        self.query_string = q_strings

    def get_request_method(self) -> HttpMethod:
        """Gets the HTTP method of the request."""
        return self.request_type

    def get_full_url(self) -> str:
        """Gets the full URI of the request."""
        return self.full_uri

    def get_headers(self) -> Dict[str, str]:
        """Gets the request headers."""
        return self.headers

    def set_header(self, header: CaseInsensitiveDict[str]):
        """Sets a request header."""
        self.headers.update(header)

    def get_body(self) -> Dict[str, str]:
        """Gets the request body."""
        return self.body

    def set_body(self, body: Dict[str, str]):
        """Sets the request body."""
        self.body = body

    def set_request_method(self, method: HttpMethod):
        """Sets the HTTP method of the request."""
        self.request_type = method

    def set_full_url(self, full_uri: str):
        """Sets the full URI of the request."""
        if full_uri:
            self.full_uri = full_uri

    def set_url_strip_right(self, toggle: bool):
        """Sets whether to strip the right side of the URL."""
        self.__strip_right_url = toggle

    def get_url_strip_right(self) -> bool:
        """Gets whether to strip the right side of the URL."""
        return self.__strip_right_url

    def set_authorization(self, auth: Dict[str, str]):
        """Sets the authentication credentials."""
        self.auth = auth

    def get_authorization(self) -> Optional[Dict[str, str]]:
        """Gets the authentication credentials."""
        return self.auth
