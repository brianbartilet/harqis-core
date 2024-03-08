from abc import ABC
import requests
import urllib.parse as url_helper
from typing import TypeVar, Type, Optional, Dict

from utilities.logging.custom_logger import custom_logger

from web.services.core.contracts.client import IWebClient
from web.services.core.contracts.service import IWebServiceRequest
from web.services.core.response import IResponse, Response

T = TypeVar('T')


class BaseWebClient(IWebClient, ABC):
    def __init__(
        self,
        base_url: str,
        *,
        response_encoding: str = "ascii",
        verify_ssh: bool = True,
        use_session: bool = False,
        cookies: Optional[Dict[str, str]] = None,
        timeout: int = 5,
        proxies: Optional[Dict[str, str]] = None,
        **kwargs
    ):
        self.log = custom_logger('Generic Web Client')

        self.base_url = base_url.rstrip('/')
        self.response_encoding = response_encoding
        self.verify_ssh = verify_ssh
        self.session = requests.Session() if use_session else None
        self.cookies = cookies or {}
        self.timeout = timeout
        self.proxies = proxies or {}

        self.config = kwargs

    def set_request_timeout(self, timeout: int) -> None:
        if timeout is not None:
            self.timeout = timeout

    def set_session_cookies(self, cookies: Dict[str, str]) -> None:
        if self.session:
            self.session.cookies.update(cookies)

    def set_cookie_handler(self, cookies: Dict[str, str]) -> None:
        if cookies is not None:
            self.cookies = cookies

    def execute_request(self, request: IWebServiceRequest, type_hook: Type[T], **kwargs) -> IResponse[T]:
        session = self.session or requests
        raw_url = self.__get_raw_url__(request.get_full_url())

        try:
            response = session.request(
                request.get_request_method().value,
                raw_url,
                cookies=self.cookies,
                verify=self.verify_ssh,
                timeout=self.timeout,
                params=request.get_query_strings(),
                headers=request.get_headers(),
                auth=request.get_authorization(),
                proxies=self.proxies,
                **request.get_body(),
                **kwargs
            )
        except Exception as e:
            self.log.error("Error sending %s request: %s", request.get_request_method().value, e)
            raise e

        return self.get_response(response, type_hook)

    def get_response(self, response: requests.Response, type_hook: Type[T]) -> IResponse[T]:
        result = Response(type_hook, data=None, response_encoding=self.response_encoding)
        result.set_status_code(response.status_code)
        result.set_headers(response.headers)
        result.set_raw_data(response.content)
        return result

    def __get_raw_url__(self, url_path_without_base: str, param_str: str = "", strip_right: bool = False) -> str:
        cleaned_url = url_path_without_base.strip("/")
        if param_str:
            cleaned_url += f"/{param_str}"

        full_url = url_helper.urljoin(self.base_url + "/", cleaned_url)
        return full_url.rstrip("/") if strip_right else full_url
