from web.services.core.contracts.constants.http_methods import Method
from web.services.core.contracts.interfaces.request import IWebServiceRequest


class RestRequest(IWebServiceRequest):

    def __init__(self):
        self.__body = {}
        self.__full_uri = ""
        self.__request_type = None
        self.__headers = {}
        self.__query_string = {}
        self.__strip_right_url = True

    def get_query_strings(self) -> dict:
        return self.__query_string

    def set_query_string(self, q_strings: dict):
        if q_strings is not None:
            self.__query_string = q_strings

    def get_request_type(self) -> Method:
        return self.__request_type

    def get_full_url(self) -> str:
        return self.__full_uri

    def get_headers(self) -> dict:
        return self.__headers

    def set_header(self, header: dict):
        if header is not None:
            self.__headers = {str(k): str(header[k]) for k in header}

    def get_body(self) -> dict:
        return self.__body

    def set_body(self, body: dict):
        if body is not None:
            self.__body = body

    def set_request_type(self, method: Method):
        self.__request_type = method

    def set_url_params(self, full_uri: str):
        if full_uri is not None or len(full_uri) > 0:
            self.__full_uri = full_uri

    def strip_right_url(self, toggle):
        self.__strip_right_url = toggle

    def get_strip_right_url_toggle(self):
        return self.__strip_right_url