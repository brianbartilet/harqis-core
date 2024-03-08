import pprint

from requests.structures import CaseInsensitiveDict

from web.services.core.contracts.request_builder import IWebRequestBuilder
from web.services.core.constants import PayloadType
from web.services.core.contracts.request import IWebServiceRequest

from web.services.core.constants.http_headers import HttpHeaders
from web.services.core.constants.http_methods import HttpMethod

from web.services.core.request import Request

from utilities.json_util import JsonObject
from utilities.logging.custom_logger import custom_logger


class RequestBuilder(IWebRequestBuilder):

    def __init__(self, routing_separator="/"):
        self.log = custom_logger('Request Builder')

        self._routing_separator = routing_separator
        self._header = CaseInsensitiveDict()
        self._query_strings = {}
        self._uri_params = []
        self._body = None
        self._method = None

        self.strip_right_url_path = True

    def set_method(self, method: HttpMethod)-> IWebRequestBuilder:
        self._method = method
        return self

    def add_header(self, header_key: HttpHeaders, header_value: str) -> IWebRequestBuilder:
        if header_key in self._header:
            self.log.debug(f"Header {header_key} already exists. Old value: {self._header[header_key.value]}, New Value: {header_value}")
        self._header[header_key.value] = header_value
        return self

    def add_headers(self, headers: dict) -> IWebRequestBuilder:
        self._header.update(headers)
        return self

    def add_payload(self, payload, payload_type: PayloadType) -> "IWebRequestBuilder":
        if self._body is None:
            self._body = {payload_type.value: payload}
        return self

    def add_file_payload(self, filename: str, filebytes: bytearray) -> "IWebRequestBuilder":
        if self._body is None and filename is not None and filebytes is not None:
            self._body = {PayloadType.FILE.value: (filename, filebytes)}
        return self

    def add_json_object(self, payload: JsonObject) -> "IWebRequestBuilder":
        if self._body is None and payload is not None:
            self._body = {PayloadType.JSON.value: payload.get_json()}
        return self

    def add_json_body(self, payload: JsonObject) -> "IWebRequestBuilder":
        if self._body is None and payload is not None:
            self._body = {PayloadType.UNKNOWN.value: payload.get_json()}
        return self

    def add_json_payload(self, payload) -> "IWebRequestBuilder":
        if self._body is None:
            self._body = {PayloadType.JSON.value: payload}
        return self

    def build(self) -> IWebServiceRequest:
        request = Request()

        self.log.debug(
            f"PROCESSING REQUEST:\n"
            f"Headers:\n{pprint.pformat(self._header)}\n"
            f"Query strings:\n{pprint.pformat(self._query_strings)}\n"
            f"URI params:\n{pprint.pformat(self._uri_params)}"
        )
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
        if query_name in self._query_strings.keys():
            self.log.warning("query parameter '%s' already exists", query_name)

        self._query_strings[query_name] = query_value
        return self

    def add_query_strings(self, **kwargs) -> "IWebRequestBuilder":
        for query in kwargs:
            self.add_query_string(query, kwargs[query])

        return self

    def add_query_object(self, target) -> "IWebRequestBuilder":

        queries = target.__dict__
        for query in queries:
            self.add_query_string(query, queries[query])

        return self

    def add_uri_parameter(self, url_param_name, url_param_value=None, order: int = None) -> IWebRequestBuilder:
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
        self.strip_right_url_path = toggle

    def __initialize__(self):
        self._method = None
        self._header = {}
        self._query_strings = {}
        self._uri_params = []
        self._body = None

    def __get_uri_param__(self):
        return "{}".format(self._routing_separator).join([str(i[1]) for i in self._uri_params])
