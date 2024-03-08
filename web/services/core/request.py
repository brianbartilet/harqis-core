from abc import ABC
from typing import Optional, Dict

from requests.structures import CaseInsensitiveDict

from web.services.core.constants.http_methods import HttpMethod
from web.services.core.contracts.request import IWebServiceRequest

from utilities.logging.custom_logger import custom_logger

class Request(IWebServiceRequest, ABC):
    def __init__(self, **kwargs):
        self.log = custom_logger('Web Request')

        self.body: Dict[str, str] = kwargs.get('body', {})
        self.full_uri: str = kwargs.get('full_uri', "")
        self.request_type: HttpMethod = kwargs.get('request_type', HttpMethod.GET)
        self.headers: Dict[str, str] = kwargs.get('headers', {})
        self.query_string: Dict[str, str] = kwargs.get('query_string', {})
        self.__strip_right_url: bool = True
        self.auth: Optional[Dict[str, str]] = kwargs.get('auth', None)

    def get_query_strings(self) -> Dict[str, str]:
        return self.query_string

    def set_query_string(self, q_strings: Dict[str, str]):
        self.query_string = q_strings

    def get_request_method(self) -> HttpMethod:
        return self.request_type

    def get_full_url(self) -> str:
        return self.full_uri

    def get_headers(self) -> Dict[str, str]:
        return self.headers

    def set_header(self, header: CaseInsensitiveDict[str]):
        self.headers.update(header)

    def get_body(self) -> Dict[str, str]:
        return self.body

    def set_body(self, body: Dict[str, str]):
        self.body = body

    def set_request_method(self, method: HttpMethod):
        self.request_type = method

    def set_full_url(self, full_uri: str):
        if full_uri:
            self.full_uri = full_uri

    def set_url_strip_right(self, toggle: bool):
        self.__strip_right_url = toggle

    def get_url_strip_right(self) -> bool:
        return self.__strip_right_url

    def set_authorization(self, auth: Dict[str, str]):
        self.auth = auth

    def get_authorization(self) -> Optional[Dict[str, str]]:
        return self.auth
