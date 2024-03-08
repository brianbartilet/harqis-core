from abc import ABC, abstractmethod
from typing import Dict, Optional

from web.services.core.constants.http_methods import HttpMethod


class IWebServiceRequest(ABC):
    """
    Interface for a web service request.
    """

    @abstractmethod
    def set_request_method(self, method: HttpMethod):
        """
        Set the HTTP method for the request.

        :param method: The HttpMethod enum value.
        """
        ...

    @abstractmethod
    def get_request_method(self) -> HttpMethod:
        """
        Get the HTTP method for the request.

        :return: The HttpMethod enum value.
        """
        ...

    @abstractmethod
    def set_header(self, header: Dict[str, str]):
        """
        Set the headers for the request.

        :param header: A dictionary of header names and values.
        """
        ...

    @abstractmethod
    def set_body(self, body: Dict[str, str]):
        """
        Set the body for the request.

        :param body: A dictionary representing the request body.
        """
        ...

    @abstractmethod
    def set_full_url(self, full_uri: str):
        """
        Set the full URL for the request.

        :param full_uri: The full URL as a string.
        """
        ...

    @abstractmethod
    def set_query_string(self, query_strings: Dict[str, str]):
        """
        Set the query string parameters for the request.

        :param query_strings: A dictionary of query string parameters.
        """
        ...

    @abstractmethod
    def get_headers(self) -> Dict[str, str]:
        """
        Get the headers for the request.

        :return: A dictionary of header names and values.
        """
        ...

    @abstractmethod
    def get_body(self) -> Optional[Dict[str, str]]:
        """
        Get the body for the request.

        :return: A dictionary representing the request body, or None if not set.
        """
        ...

    @abstractmethod
    def get_full_url(self) -> str:
        """
        Get the full URL for the request.

        :return: The full URL as a string.
        """
        ...

    @abstractmethod
    def get_query_strings(self) -> Dict[str, str]:
        """
        Get the query string parameters for the request.

        :return: A dictionary of query string parameters.
        """
        ...

    @abstractmethod
    def set_url_strip_right(self, toggle: bool):
        """
        Set whether to strip the rightmost slash from the URL.

        :param toggle: True to strip the slash, False to keep it.
        """
        ...

    @abstractmethod
    def get_url_strip_right(self) -> bool:
        """
        Get whether the rightmost slash from the URL is stripped.

        :return: True if the slash is stripped, False otherwise.
        """
        ...

    @abstractmethod
    def set_authorization(self, authorization: Dict[str, str]):
        """
        Set the authorization headers for the request.

        :param authorization: A dictionary of authorization headers.
        """
        ...

    @abstractmethod
    def get_authorization(self) -> Optional[Dict[str, str]]:
        """
        Get the authorization headers for the request.

        :return: A dictionary of authorization headers, or None if not set.
        """
        ...
