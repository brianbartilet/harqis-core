from abc import ABC, abstractmethod

from web.services.core.constants.payload_type import PayloadType
from web.services.core.constants.http_methods import HttpMethod

from web.services.core.contracts.request import IWebServiceRequest

from utilities.json_util import JsonObject

from requests.structures import CaseInsensitiveDict

class IWebRequestBuilder(ABC):
    """
    Interface for a chainable web request builder.
    """

    def set_method(self, method: HttpMethod)-> "IWebRequestBuilder":
        """
        Set request http method

        :param method: http method
        """
        ...

    @abstractmethod
    def add_header(self, header_key: str, header_value: str) -> "IWebRequestBuilder":
        """
        Adds a single header to the request.

        :param header_key: The key of the header.
        :param header_value: The value of the header.
        :return: The builder instance for chaining.
        """
        ...

    @abstractmethod
    def add_headers(self, headers: CaseInsensitiveDict[str]) -> "IWebRequestBuilder":
        """
        Adds multiple headers to the request.

        :param headers: A dictionary of headers.
        :return: The builder instance for chaining.
        """
        ...

    @abstractmethod
    def add_payload(self, payload, payload_type: PayloadType) -> "IWebRequestBuilder":
        """
        Adds a payload to the request with a specified type.

        :param payload: The payload to add.
        :param payload_type: The type of the payload.
        :return: The builder instance for chaining.
        """
        ...

    @abstractmethod
    def add_file_payload(self, filename: str, filebytes: bytearray) -> "IWebRequestBuilder":
        """
        Adds a file payload to the request.

        :param filename: The name of the file.
        :param filebytes: The bytes of the file.
        :return: The builder instance for chaining.
        """
        ...

    @abstractmethod
    def add_json_object(self, payload: JsonObject) -> "IWebRequestBuilder":
        """
        Adds a JSON object to the request.

        :param payload: The JSON object to add.
        :return: The builder instance for chaining.
        """
        ...

    @abstractmethod
    def add_json_body(self, payload: JsonObject) -> "IWebRequestBuilder":
        """
        Adds a JSON body to the request.

        :param payload: The JSON object to use as the body.
        :return: The builder instance for chaining.
        """
        ...

    @abstractmethod
    def add_json_payload(self, payload) -> "IWebRequestBuilder":
        """
        Adds a JSON payload to the request.

        :param payload: The payload to add.
        :return: The builder instance for chaining.
        """
        ...

    @abstractmethod
    def add_uri_parameter(self, param_name: str, param_value=None, order: int = None) -> "IWebRequestBuilder":
        """
        Adds a URI parameter to the request.

        :param param_name: The name of the parameter.
        :param param_value: The value of the parameter.
        :param order: The order of the parameter in the URI.
        :return: The builder instance for chaining.
        """
        ...

    @abstractmethod
    def add_query_string(self, query_name: str, query_value) -> "IWebRequestBuilder":
        """
        Adds a query string to the request.

        :param query_name: The name of the query string.
        :param query_value: The value of the query string.
        :return: The builder instance for chaining.
        """
        ...

    @abstractmethod
    def add_query_strings(self, **kwargs) -> "IWebRequestBuilder":
        """
        Adds multiple query strings to the request.

        :param kwargs: Keyword arguments representing query string names and values.
        :return: The builder instance for chaining.
        """
        ...

    @abstractmethod
    def add_query_object(self, object) -> "IWebRequestBuilder":
        """
        Adds an object as query strings to the request.

        :param object: The object to add as query strings.
        :return: The builder instance for chaining.
        """
        ...

    @abstractmethod
    def strip_right_url(self, toggle: bool = True) -> "IWebRequestBuilder":
        """
        Toggles stripping the rightmost slash from the URL.

        :param toggle: True to strip the slash, False to keep it.
        :return: The builder instance for chaining.
        """
        ...

    @abstractmethod
    def build(self) -> IWebServiceRequest:
        """
        Builds the web service request.

        :return: The constructed IWebServiceRequest instance.
        """
        ...
