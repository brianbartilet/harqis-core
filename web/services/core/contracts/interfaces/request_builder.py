from abc import abstractmethod

from web.services.core.contracts.constants.payload_type import PayloadType
from web.services.core.contracts.interfaces.request import IWebServiceRequest

from utilities.json_util import JsonObject


class IWebRequestBuilder:
    @abstractmethod
    def add_header(self, header_key, header_value) -> "IWebRequestBuilder":
        ...

    @abstractmethod
    def add_headers(self, headers: dict) -> "IWebRequestBuilder":
        ...

    # there might be a type here - > json or non-json
    @abstractmethod
    def add_payload(self, payload, payload_type: PayloadType) -> "IWebRequestBuilder":
        ...

    @abstractmethod
    def add_file_payload(self, filename: str, filebytes: bytearray) -> "IWebRequestBuilder":
        ...

    @abstractmethod
    def add_json_object(self, payload: JsonObject) -> "IWebRequestBuilder":
        ...

    @abstractmethod
    def add_json_body(self, payload: JsonObject) -> "IWebRequestBuilder":
        ...

    @abstractmethod
    def add_json_payload(self, payload) -> "IWebRequestBuilder":
        ...

    @abstractmethod
    def add_uri_parameter(self, param_name, param_value=None, order: int = None) -> "IWebRequestBuilder":
        ...

    @abstractmethod
    def add_query_string(self, query_name, query_value) -> "IWebRequestBuilder":
        ...

    @abstractmethod
    def add_query_strings(self, **kwargs) -> "IWebRequestBuilder":
        ...


    @abstractmethod
    def add_query_object(self, object) -> "IWebRequestBuilder":
        ...

    @abstractmethod
    def strip_right_url(self, toggle=True):
        ...

    @abstractmethod
    def build(self) -> IWebServiceRequest:
        """

        :return:
        """
        ...
