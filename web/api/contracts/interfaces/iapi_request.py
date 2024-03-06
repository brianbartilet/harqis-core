from abc import abstractmethod

from web.api.contracts.constants.http_methods import Method


class IApiRequest:

    # TODO: IApiRequest
    @abstractmethod
    def set_request_type(self, method: Method):
        ...

    @abstractmethod
    def get_request_type(self) -> Method:
        ...

    @abstractmethod
    def set_header(self, header: dict):
        ...

    @abstractmethod
    def set_body(self, body):
        ...

    @abstractmethod
    def set_url_params(self, full_uri: str):
        ...

    @abstractmethod
    def set_query_string(self, q_strings: dict):
        ...

    @abstractmethod
    def get_headers(self) -> dict:
        ...

    @abstractmethod
    def get_body(self) -> dict:
        ...

    @abstractmethod
    def get_full_url(self) -> str:
        ...

    @abstractmethod
    def get_query_strings(self) -> dict:
        ...

    @abstractmethod
    def strip_right_url(self, toggle):
        ...

    @abstractmethod
    def get_strip_right_url_toggle(self) -> bool:
        ...
