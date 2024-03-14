from requests.structures import CaseInsensitiveDict

from web.services.core.contracts.request_builder import IWebRequestBuilder
from web.services.core.contracts.request import IWebServiceRequest

from web.services.core.constants.payload_type import PayloadType
from web.services.core.constants.http_headers import HttpHeaders
from web.services.core.constants.http_methods import HttpMethod

from web.services.core.request import Request

from web.services.core.json import JsonObject
from utilities.logging.custom_logger import create_logger


class RequestBuilder(IWebRequestBuilder):
    """
    A builder class for constructing web service requests.
    """

    def __init__(self, **kwargs):
        """
        Initializes the RequestBuilder.

        Args:
            routing_separator: The separator used in the URI routing. Defaults to "/".
        """
        self.log = kwargs.get('logger', create_logger(self.__class__.__name__))
        self.routing_separator = kwargs.get('routing_separator', "/")

        self._header = CaseInsensitiveDict()
        self._query_strings = {}
        self._uri_params = []
        self._body = None
        self._method = None

        self.strip_right_url_path = True

    def set_method(self, method: HttpMethod) -> IWebRequestBuilder:
        """
        Sets the HTTP method for the request.

        Args:
            method: The HttpMethod to be used for the request.

        Returns:
            The builder instance for chaining.
        """
        self._method = method
        return self

    def add_header(self, header_key: HttpHeaders, header_value: str) -> IWebRequestBuilder:
        """
        Adds a single header to the request.

        Args:
            header_key: The key of the header.
            header_value: The value of the header.

        Returns:
            The builder instance for chaining.
        """
        if header_key.value in self._header:
            self.log.debug(f"Header {header_key} already exists. Old value: {self._header[header_key.value]}, "
                           f"New Value: {header_value}")
        self._header[header_key.value] = header_value

        return self

    def add_headers(self, headers: dict) -> IWebRequestBuilder:
        """
        Adds multiple headers to the request.

        Args:
            headers: A dictionary of headers.

        Returns:
            The builder instance for chaining.
        """
        self._header.update(headers)

        return self

    def add_payload(self, payload, payload_type: PayloadType) -> IWebRequestBuilder:
        """
        Adds a payload to the request with a specified type.

        Args:
            payload: The payload to add.
            payload_type: The type of the payload.

        Returns:
            The builder instance for chaining.
        """
        if self._body is None:
            self._body = {payload_type.value: payload}

        return self

    def add_file_payload(self, filename: str, filebytes: bytearray) -> IWebRequestBuilder:
        """
        Adds a file payload to the request.

        Args:
            filename: The name of the file.
            filebytes: The bytes of the file.

        Returns:
            The builder instance for chaining.
        """
        if self._body is None and filename is not None and filebytes is not None:
            self._body = {PayloadType.FILE.value: (filename, filebytes)}

        return self

    def add_json_object(self, payload: JsonObject) -> IWebRequestBuilder:
        """
        Adds a JSON object to the request.

        Args:
            payload: The JSON object to add.

        Returns:
            The builder instance for chaining.
        """
        if self._body is None and payload is not None:
            self._body = {PayloadType.JSON.value: payload.get_json()}

        return self

    def add_json_body(self, payload: JsonObject) -> IWebRequestBuilder:
        """
        Adds a JSON body to the request.

        Args:
            payload: The JSON object to use as the body.

        Returns:
            The builder instance for chaining.
        """
        if self._body is None and payload is not None:
            self._body = {PayloadType.UNKNOWN.value: payload.get_json()}

        return self

    def add_json_payload(self, payload) -> IWebRequestBuilder:
        """
        Adds a JSON payload to the request.

        Args:
            payload: The payload to add.

        Returns:
            The builder instance for chaining.
        """
        if self._body is None:
            self._body = {PayloadType.JSON.value: payload}

        return self

    def build(self) -> IWebServiceRequest:
        """
        Builds the web service request.

        Returns:
            The constructed IWebServiceRequest instance.
        """
        request = Request()

        if self._method:
            request.set_request_method(self._method)
        if self._header:
            request.set_header(self._header)
        if self._body:
            request.set_body(self._body)
        if self._query_strings:
            request.set_query_string(self._query_strings)

        uri_string = self.__get_uri_param__()
        request.set_full_url(uri_string)
        request.set_url_strip_right(self.strip_right_url_path)

        self.__initialize__()

        return request

    def add_query_string(self, query_name, query_value) -> IWebRequestBuilder:
        """
        Adds a query string to the request.

        Args:
            query_name: The name of the query string.
            query_value: The value of the query string.

        Returns:
            The builder instance for chaining.
        """
        if query_name in self._query_strings.keys():
            self.log.warning("query parameter '%s' already exists", query_name)

        self._query_strings[query_name] = query_value

        return self

    def add_query_strings(self, **kwargs) -> IWebRequestBuilder:
        """
        Adds multiple query strings to the request.

        Args:
            kwargs: Keyword arguments representing query string names and values.

        Returns:
            The builder instance for chaining.
        """
        for query in kwargs:
            self.add_query_string(query, kwargs[query])

        return self

    def add_query_object(self, target) -> IWebRequestBuilder:
        """
        Adds an object as query strings to the request.

        Args:
            target: The object to add as query strings.

        Returns:
            The builder instance for chaining.
        """
        queries = target.__dict__
        for query in queries:
            self.add_query_string(query, queries[query])

        return self

    def add_uri_parameter(self, url_param_name, url_param_value=None, order: int = None) -> IWebRequestBuilder:
        """
        Adds a URI parameter to the request.

        Args:
            url_param_name: The name of the parameter.
            url_param_value: The value of the parameter.
            order: The order of the parameter in the URI.

        Returns:
            The builder instance for chaining.
        """
        parameter_dict = {i[0]: i[1] for i in self._uri_params}
        new_order = (order, len(self._uri_params))[order is None]

        if url_param_name in parameter_dict.keys():
            old_value = parameter_dict[url_param_name]
            self.log.warning("URI parameter already exists. Old value(order): %s(%s), New Value(order): %s(%s)",
                              old_value, self._uri_params.index((url_param_name, old_value)), url_param_value, new_order)
            self._uri_params.remove((url_param_name, old_value))

        if url_param_value is None:
            self._uri_params.insert(new_order, (url_param_name, url_param_name))
        else:
            self._uri_params.insert(new_order, (url_param_name, url_param_value))

        return self

    def strip_right_url(self, toggle=True):
        """
        Toggles stripping the rightmost slash from the URL.

        Args:
            toggle: True to strip the slash, False to keep it.
        """
        self.strip_right_url_path = toggle

    def __initialize__(self):
        """
        Reinitializes the builder instance to its default state.
        """
        self._method = None
        self._header = {}
        self._query_strings = {}
        self._uri_params = []
        self._body = None

    def __get_uri_param__(self):
        """
        Constructs the URI parameter string.

        Returns:
            The URI parameter string.
        """
        return "{}".format(self.routing_separator).join([str(i[1]) for i in self._uri_params])
