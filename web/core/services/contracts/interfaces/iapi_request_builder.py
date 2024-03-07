from abc import abstractmethod

from web.core.services.contracts.constants.payload_type import PayloadType
from web.core.services.contracts.interfaces.iapi_request import IApiRequest
from utilities.json_util import JsonObject


class IApiRequestBuilder:
    @abstractmethod
    def add_header(self, header_key, header_value) -> "IApiRequestBuilder":
        ...

    @abstractmethod
    def add_headers(self, headers: dict) -> "IApiRequestBuilder":
        ...

    # there might be a type here - > json or non-json
    @abstractmethod
    def add_payload(self, payload, payload_type: PayloadType) -> "IApiRequestBuilder":
        ...

    @abstractmethod
    def add_file_payload(self, filename: str, filebytes: bytearray) -> "IApiRequestBuilder":
        ...

    @abstractmethod
    def add_json_object(self, payload: JsonObject) -> "IApiRequestBuilder":
        ...

    @abstractmethod
    def add_json_body(self, payload: JsonObject) -> "IApiRequestBuilder":
        ...

    @abstractmethod
    def add_json_payload(self, payload) -> "IApiRequestBuilder":
        ...

    @abstractmethod
    def add_uri_parameter(self, param_name, param_value=None, order: int = None) -> "IApiRequestBuilder":
        ...

    @abstractmethod
    def add_query_string(self, query_name, query_value) -> "IApiRequestBuilder":
        ...

    @abstractmethod
    def add_query_strings(self, **kwargs) -> "IApiRequestBuilder":
        ...


    @abstractmethod
    def add_query_object(self, object) -> "IApiRequestBuilder":
        ...

    @abstractmethod
    def strip_right_url(self, toggle=True):
        ...

    @abstractmethod
    def build(self) -> IApiRequest:
        """

        :return:
        """
        ...
