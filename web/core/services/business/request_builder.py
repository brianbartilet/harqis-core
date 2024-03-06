from web.core.services.contracts.interfaces.iapi_request_builder import IApiRequestBuilder

from web.core.services.contracts.base.api_request import RestRequest
from web.core.services.contracts.constants.payload_type import PayloadType
from web.core.services.contracts.interfaces.iapi_request import IApiRequest
from utilities.json_util import JsonObject
from utilities.custom_logger import custom_logger
from enum import Enum

import pprint

log = custom_logger('REQUEST BUILDER')


class HttpHeaders(Enum):
    ACCEPT = 'Accept'
    ACCEPT_CHARSET = 'Accept-Charset'
    AUTHORIZATION = 'Authorization'
    CONTENT_TYPE = 'Content-Type'
    ORIGIN = 'Origin'
    USER_AGENT = 'User-Agent'
    CACHE_CONTROL = 'Cache-Control'
    CONNECTION = 'Connection'
    ACCEPT_ENCODING = 'Accept-Encoding'
    HOST = 'Host'
    REFERER = 'Referer'
    X_REQUESTED_WITH = 'X-Requested-With'
    COOKIE = 'Cookie'

class RequestBuilder(IApiRequestBuilder):

    def __init__(self, routing_separator="/"):

        self._routing_separator = routing_separator
        self._header = {}
        self._query_strings = {}
        self._uri_params = []
        self._body = None
        self._method = None
        self._strip_right_url = True

    def add_header(self, header_key: HttpHeaders, header_value) -> IApiRequestBuilder:
        if header_key in self._header.keys():
            log.debug("query parameter already exists. Old value: %s, New Value: %s",
                            self._header[header_key], header_value)
        self._header[header_key] = header_value
        return self

    def add_headers(self, headers: dict) -> IApiRequestBuilder:
        for header in headers:
            self.add_header(**header)

        return self

    def add_payload(self, payload, payload_type: PayloadType) -> "IApiRequestBuilder":
        if self._body is None:
            self._body = {payload_type.value: payload}
        return self

    def add_file_payload(self, filename: str, filebytes: bytearray) -> "IApiRequestBuilder":
        if self._body is None and filename is not None and filebytes is not None:
            self._body = {PayloadType.FILE.value: (filename, filebytes)}
        return self

    def add_json_object(self, payload: JsonObject) -> "IApiRequestBuilder":
        if self._body is None and payload is not None:
            self._body = {PayloadType.JSON.value: payload.get_json()}
        return self

    def add_json_body(self, payload: JsonObject) -> "IApiRequestBuilder":
        if self._body is None and payload is not None:
            self._body = {PayloadType.UNKNOWN.value: payload.get_json()}
        return self

    def add_json_payload(self, payload) -> "IApiRequestBuilder":
        if self._body is None:
            self._body = {PayloadType.JSON.value: payload}
        return self

    def build(self) -> IApiRequest:
        request = RestRequest()

        if self._header is not None:
            request.set_header(self._header)
        if self._body is not None:
            request.set_body(self._body)

        if self._query_strings is not None:
            request.set_query_string(self._query_strings)

        uri_string = self.__get_uri_param__()
        request.set_url_params(uri_string)
        request.strip_right_url(self._strip_right_url)

        log.info("PROCESSING REQUEST:")
        log.info("Showing headers:\n" + pprint.pformat(self._header))

        log.info("Showing query strings:\n" + pprint.pformat(self._query_strings))
        log.info("Showing uri params:\n" + pprint.pformat(self._uri_params))

        self.__initialize__()

        return request

    def add_query_string(self, query_name, query_value) -> IApiRequestBuilder:
        if query_name in self._query_strings.keys():
            #  self._log.warning("query parameter already exists. Old value: %s, New Value: %s",
            #                    self._query_strings[query_name], query_value)
            log.warning("query parameter '%s' already exists", query_name)

        self._query_strings[query_name] = query_value
        return self

    def add_query_strings(self, **kwargs) -> "IApiRequestBuilder":
        for query in kwargs:
            self.add_query_string(query, kwargs[query])

        return self

    def add_query_object(self, object) -> "IApiRequestBuilder":

        queries = object.__dict__
        for query in queries:
            self.add_query_string(query, queries[query])

        return self

    def add_uri_parameter(self, url_param_name, url_param_value=None, order: int = None) -> IApiRequestBuilder:
        parameter_dict = {i[0]: i[1] for i in self._uri_params}
        new_order = (order, len(self._uri_params))[order is None]

        if url_param_name in parameter_dict.keys():
            old_value = parameter_dict[url_param_name]
            log.warning("URI parameter already exists. Old value(order): %s(%s), New Value(order): %s(%s)",
                              old_value, self._uri_params.index((url_param_name, old_value)), url_param_value, new_order)
            self._uri_params.remove((url_param_name, old_value))

        if url_param_value is None:
            self._uri_params.insert(new_order, (url_param_name, url_param_name))
        else:
            self._uri_params.insert(new_order, (url_param_name, url_param_value))

        return self

    def strip_right_url(self, toggle=True):
        self._strip_right_url = toggle

    def __initialize__(self):
        self._header = {}
        self._query_strings = {}
        self._uri_params = []
        self._body = None

    def __get_uri_param__(self):
        return "{}".format(self._routing_separator).join([str(i[1]) for i in self._uri_params])
