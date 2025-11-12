from requests.structures import CaseInsensitiveDict

from core.web.services.core.contracts.request_builder import IWebRequestBuilder
from core.web.services.core.contracts.request import IWebServiceRequest

from core.web.services.core.constants.payload_type import PayloadType
from core.web.services.core.constants.http_methods import HttpMethod

from core.web.services.core.request import Request

from core.web.services.core.json import JsonObject
from core.utilities.logging.custom_logger import create_logger

from enum import Enum
from typing import TypeVar, List

THeader = TypeVar("THeader")


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
        self._uri_params: List[tuple[str, str]] = []
        self._body = None
        self._method = None

        # NEW: remember base path segments, e.g. ["product"]
        self._base_segments: List[str] = []

        self.strip_right_url_path = True

        self.kwargs = kwargs

    # ─────────────────────────────────────────────────────────────
    # HTTP Methods
    # ─────────────────────────────────────────────────────────────
    def get(self):
        """
        Sets the HTTP method to GET.
        """
        return self.set_method(HttpMethod.GET)

    def post(self):
        """
        Sets the HTTP method to POST.
        """
        return self.set_method(HttpMethod.POST)

    def put(self):
        """
        Sets the HTTP method to PUT.
        """
        return self.set_method(HttpMethod.PUT)

    def delete(self):
        """
        Sets the HTTP method to DELETE.
        """
        return self.set_method(HttpMethod.DELETE)

    def patch(self):
        """
        Sets the HTTP method to PATCH.
        """
        return self.set_method(HttpMethod.PATCH)

    def head(self):
        """
        Sets the HTTP method to HEAD.
        """
        return self.set_method(HttpMethod.HEAD)

    def options(self):
        """
        Sets the HTTP method to OPTIONS.
        """
        return self.set_method(HttpMethod.OPTIONS)

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

    # ─────────────────────────────────────────────────────────────
    # Headers
    # ─────────────────────────────────────────────────────────────
    def add_header(self, header_key: THeader, header_value: str) -> IWebRequestBuilder:
        """
        Adds a single header to the request.

        Args:
            header_key: The key of the header defined from set of keys or string.
            header_value: The value of the header.

        Returns:
            The builder instance for chaining.
        """

        if isinstance(header_key, Enum):
            key = header_key.value
        else:
            key = header_key

        if key in self._header:
            self.log.debug(
                f"Header {header_key} already exists. "
                f"Old value: {self._header[key]}, New Value: {header_value}"
            )
        self._header[key] = header_value
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

    # NEW: optional clearers to play nice with client cleanup (no-op if you don’t use them)
    def clear_headers(self) -> IWebRequestBuilder:
        self._header = CaseInsensitiveDict()
        return self

    # ─────────────────────────────────────────────────────────────
    # Payload
    # ─────────────────────────────────────────────────────────────
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

    # NEW: optional clearer
    def clear_body(self) -> IWebRequestBuilder:
        self._body = None
        return self

    # ─────────────────────────────────────────────────────────────
    # Query strings
    # ─────────────────────────────────────────────────────────────
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

    # NEW: optional clearer
    def clear_query_strings(self) -> IWebRequestBuilder:
        self._query_strings = {}
        return self

    # ─────────────────────────────────────────────────────────────
    # URI
    # ─────────────────────────────────────────────────────────────
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
            self.log.warning(
                "URI parameter already exists. "
                "Old value(order): %s(%s), New Value(order): %s(%s)",
                old_value, self._uri_params.index((url_param_name, old_value)),
                url_param_value, new_order
            )
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

    # NEW: define a base path like ["product"] and apply it
    def set_base_uri(self, *segments: str) -> IWebRequestBuilder:
        self._base_segments = [str(s).strip("/") for s in segments if s]
        self._reset_uri_to_base()
        return self

    # NEW: clear all URI segments
    def _clear_uri_parameters(self) -> IWebRequestBuilder:
        self._uri_params = []
        return self

    # NEW: reset URI segments back to the configured base
    def _reset_uri_to_base(self) -> IWebRequestBuilder:
        self._clear_uri_parameters()
        for seg in self._base_segments:
            self.add_uri_parameter(seg)
        return self

    # ─────────────────────────────────────────────────────────────
    # Build
    # ─────────────────────────────────────────────────────────────
    def build(self, clear_all=False) -> IWebServiceRequest:
        """
        Builds the web service request.
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

        # IMPORTANT: after we build, reset this builder for next use:
        self.__initialize__(clear_all)

        return request

    def __initialize__(self, clear_all: bool):
        """
        Re-initializes the builder instance to its default state.
        - Always clears method, query strings, and body (per-call state).
        - Keeps headers by default.
        - Resets the URI path back to base segments (prevents path bleed).
        """
        # reset per-call properties
        self._method = None
        self._query_strings = {}
        self._body = None

        # keep headers by default; allow full clear if requested
        if clear_all:
            self._header = CaseInsensitiveDict()

        # CRUCIAL: restore path to base (so next call starts clean at /product)
        if self._base_segments:
            self.reset_uri_to_base()
        else:
            # if no base set, leave URI params as-is or clear them (choose behavior)
            # safer default: clear so callers must always add segments explicitly
            self._uri_params = []

    # utility
    def __get_uri_param__(self):
        """
        Constructs the URI parameter string.

        Returns:
            The URI parameter string.
        """
        return "{}".format(self.routing_separator).join([str(i[1]) for i in self._uri_params])
