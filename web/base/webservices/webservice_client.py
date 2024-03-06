from typing import TypeVar, Type

import requests

from web.core.services.contracts.interfaces.iapi_client import IApiClient
from web.core.services.contracts.interfaces.iapi_response import IApiResponse
from web.core.services.contracts.base.api_response import ApiResponse
from web.core.services.contracts.interfaces.iapi_request import IApiRequest
from web.core.services.raw_rest_client import RawRestClient

from utilities.custom_logger import custom_logger

from environment_variables import *

T = TypeVar("T")


class BaseApiClient(IApiClient, RawRestClient):

    def __init__(self, base_url: str, **kwargs):
        self.config = kwargs

        self.__base_url = base_url
        self.__response_encoding = kwargs.get("response_encoding", "ascii")
        self.__strip_right_url = True
        self.__default_headers = kwargs.get("default_headers", {})
        self.__timeout = kwargs.get("timeout", 5)
        self.__auth = kwargs.get("auth", None)
        self.__verify_ssh = kwargs.get("verify", False)
        self.__cookies = kwargs.get("cookies", {})
        self.__proxies = kwargs.get("proxies", {}) if str(ENV_ENABLE_PROXY).lower() == "true" else {}
        self.__session = requests.Session() if kwargs.get("use_session", False) else None
        self.__log = custom_logger()

        super(BaseApiClient, self).__init__(base_url, self.__verify_ssh, self.__response_encoding)
        self.initialize()

    def initialize(self):
        if self.__session is not None:
            pass
            #self.__session.get(self.__base_url, proxies=self.__proxies)
            #self.__cookies = self.__session.cookies.get_dict()

    def authorize(self):
        pass

    def execute(self, request_object: IApiRequest, type_hook: Type[T], **kwargs) -> IApiResponse[T]:
        actual_method = request_object.get_request_type().value
        self.__log.info("PROCESSING " + actual_method + "()")
        try:
            response = self._execute_request(request_object, **kwargs)

        except Exception as e:
            self.__log.error("Error sending %s request: %s", request_object.get_request_type().value, e)
            raise e

        return self._parse_response_(response, type_hook)

    def set_request_timeout(self, timeout: int):
        if timeout is not None:
            self.__timeout = timeout

    def set_default_headers(self, headers: dict):
        if headers is not None:
            self.__default_headers = headers

    def set_session_cookies(self, cookies: dict):
        for cookie in cookies:
            c = {cookie['name']: cookie['value']}
            self.__session.cookies.update(c)

    def set_cookie_handler(self, cookies: dict):
        if cookies is not None:
            if "cookies" in cookies.keys():
                self.__cookies = cookies
            else:
                self.__cookies = {"cookies": cookies}

    def _parse_response_(self, response: requests.Response, type_hook: Type[T]) -> IApiResponse[T]:

        result = ApiResponse(type_hook,
                             data=None,
                             response_encoding=self.__response_encoding)

        result.set_status_code(response.status_code)
        result.set_header(response.headers)
        result.set_raw_data(response.content)

        self.log.info('response hook: ' + type_hook.__name__ + ' ' + str(type_hook) + '\n')
        self.log.info('response status code: ' + str(response.status_code) + '\n')

        return result

    def _parse_request(self, request_obj):
        if self.__session is not None:
            session_object = self.__session
        else:
            session_object = requests

        headers = {**request_obj.get_headers(), **self.__default_headers}
        if not headers:
            headers = self.__default_headers

        url_path_without_base = request_obj.get_full_url()
        self.__strip_right_url = request_obj.get_strip_right_url_toggle()

        raw_url = self.__get_raw_url__(url_path_without_base, strip_right=self.__strip_right_url)

        body = request_obj.get_body()

        return session_object, raw_url, headers, body

    def _execute_request(self, request_obj: IApiRequest, **kwargs) -> requests.Response:
        method = request_obj.get_request_type().value
        session, raw_url, headers, body = self._parse_request(request_obj)

        response = session.request(
            method,
            raw_url,
            cookies=self.__cookies,
            verify=self.__verify_ssh,
            timeout=self.__timeout,
            params=request_obj.get_query_strings(),
            headers=headers,
            auth=self.__auth,
            proxies=self.__proxies,
            **body,
            **kwargs
            )

        return response