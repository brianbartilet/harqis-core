import requests
import urllib.parse as url_helper
from typing import TypeVar, Type

from utilities.json_util import JsonUtil, JsonObject
from utilities.custom_logger import custom_logger

T = TypeVar('T')


class RawRestClient:
    def __init__(self, base_url: str, verify_ssh=False, response_encoding="ascii"):
        self.log = custom_logger()
        self.base_url = base_url
        self.verify_ssh = verify_ssh
        self.cookie = None
        self.response_encoding = response_encoding

    def get_raw(self, url_path_without_base: str, param_str=None):
        raw_url = self.__get_raw_url__(url_path_without_base, param_str)
        return requests.get(raw_url, cookies=self.cookie, verify=self.verify_ssh)

    def get(self, url_path_without_base: str, param_str=None, type_hook: T = JsonObject) -> T:
        result = self.get_raw(url_path_without_base, param_str)
        j_object = JsonUtil.deserialize(result.content.decode(self.response_encoding), Type[type_hook])

        return j_object

    def post_raw(self, url_path_without_base : str, data_param : str = None):
        raw_url = self.__get_raw_url__(url_path_without_base, "")
        return requests.post(raw_url, cookies=self.cookie, verify=self.verify_ssh, data=data_param)

    def post(self, url_path_without_base : str, data_param : str = None, type_hook : T = JsonObject) -> T:
        result = self.post_raw(url_path_without_base, data_param)
        j_object = JsonUtil.deserialize(result.content.decode(self.response_encoding), type_hook)

        return j_object

    def __get_raw_url__(self, url_path_without_base : str, param_str = "", strip_right = False):
        cleaned_url = url_path_without_base.lstrip("/").rstrip("/")
        if param_str is None or len(param_str) == 0:
            cleaned_url += "/"
        else:
            cleaned_url += "/{}".format(param_str)

        temp_url = url_helper.urljoin(self.base_url, cleaned_url)
        return (temp_url,temp_url.rstrip("/"))[strip_right]