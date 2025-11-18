from abc import ABC, abstractmethod

from core.web.services.core.constants.payload_type import PayloadType
from core.web.services.core.constants.http_methods import HttpMethod
from core.web.services.core.constants.http_headers import HttpHeaders

from core.web.services.core.contracts.request import IWebServiceRequest

from core.web.services.core.json import JsonObject

from requests.structures import CaseInsensitiveDict


class IWebRequestBuilder(ABC):
    """
    Interface for a chainable web request builder.
    """

    @abstractmethod
    def set_method(self, method: HttpMethod) -> "IWebRequestBuilder":
        """
        Set the HTTP method for the request.

        Args:
            method: The HttpMethod to be used for the request.

        Returns:
            The builder instance for chaining.
        """
        ...

    @abstractmethod
    def add_header(self, header_key: HttpHeaders, header_value: str) -> "IWebRequestBuilder":
        """
        Adds a single header to the request.

        Args:
            header_key: The key of the header.
            header_value: The value of the header.

        Returns:
            The builder instance for chaining.
        """
        ...

    @abstractmethod
    def add_headers(self, headers: CaseInsensitiveDict[str]) -> "IWebRequestBuilder":
        """
        Adds multiple headers to the request.

        Args:
            headers: A dictionary of headers.

        Returns:
            The builder instance for chaining.
        """
        ...

    @abstractmethod
    def add_payload(self, payload, payload_type: PayloadType) -> "IWebRequestBuilder":
        """
        Adds a payload to the request with a specified type.

        Args:
            payload: The payload to add.
            payload_type: The type of the payload.

        Returns:
            The builder instance for chaining.
        """
        ...

    @abstractmethod
    def add_file_payload(self, filename: str, filebytes: bytearray) -> "IWebRequestBuilder":
        """
        Adds a file payload to the request.

        Args:
            filename: The name of the file.
            filebytes: The bytes of the file.

        Returns:
            The builder instance for chaining.
        """
        ...

    @abstractmethod
    def add_json_object(self, payload: JsonObject) -> "IWebRequestBuilder":
        """
        Adds a JSON object to the request.

        Args:
            payload: The JSON object to add.

        Returns:
            The builder instance for chaining.
        """
        ...

    @abstractmethod
    def add_json_body(self, payload: JsonObject) -> "IWebRequestBuilder":
        """
        Adds a JSON body to the request.

        Args:
            payload: The JSON object to use as the body.

        Returns:
            The builder instance for chaining.
        """
        ...

    @abstractmethod
    def add_json_payload(self, payload) -> "IWebRequestBuilder":
        """
        Adds a JSON payload to the request.

        Args:
            payload: The payload to add.

        Returns:
            The builder instance for chaining.
        """
        ...

    @abstractmethod
    def add_uri_parameter(self, param_name: str, param_value=None, order: int = None) -> "IWebRequestBuilder":
        """
        Adds a URI parameter to the request.

        Args:
            param_name: The name of the parameter.
            param_value: The value of the parameter.
            order: The order of the parameter in the URI.

        Returns:
            The builder instance for chaining.
        """
        ...

    @abstractmethod
    def add_query_string(self, query_name: str, query_value) -> "IWebRequestBuilder":
        """
        Adds a query string to the request.

        Args:
            query_name: The name of the query string.
            query_value: The value of the query string.

        Returns:
            The builder instance for chaining.
        """
        ...

    @abstractmethod
    def add_query_strings(self, **kwargs) -> "IWebRequestBuilder":
        """
        Adds multiple query strings to the request.

        Args:
            kwargs: Keyword arguments representing query string names and values.

        Returns:
            The builder instance for chaining.
        """
        ...

    @abstractmethod
    def add_query_object(self, object) -> "IWebRequestBuilder":
        """
        Adds an object as query strings to the request.

        Args:
            object: The object to add as query strings.

        Returns:
            The builder instance for chaining.
        """
        ...

    @abstractmethod
    def strip_right_url(self, toggle: bool = True) -> "IWebRequestBuilder":
        """
        Toggles stripping the rightmost slash from the URL.

        Args:
            toggle: True to strip the slash, False to keep it.

        Returns:
            The builder instance for chaining.
        """
        ...

    @abstractmethod
    def build(self, **kwargs) -> IWebServiceRequest:
        """
        Builds the web service request.

        Returns:
            The constructed IWebServiceRequest instance.
        """
        ...

    @abstractmethod
    def set_base_uri(self, *segments: str) -> IWebServiceRequest:
        """
        Sets the base URI for the request.
        """
        ...


