
from web.services.rest.client import RestClient

from utilities.asserts.helper import LoggedAssertHelper


from utilities.apps_context import AppConfigurationContext

from web.services.core.contracts import *
from web.services.core.constants import *
from web.services.core.request_builder import RequestBuilder

from web.services.core.dto import BaseDto
from typing import TypeVar, Type
T = TypeVar("T")
V = TypeVar("V")




class WebService(IWebService[T]):

    response_type = Type[T]
    headers = HttpHeaders

    def __init__(self,
                 source_id: str,
                 apps_config_data: dict,
                 client: type = RestClient,
                 val: Type[T] = BaseDto,
                 app_ctx: type = AppConfigurationContext,
                 app_service_type: ServiceClientType = ServiceClientType.WEBSERVICE_GENERIC,
                 **kwargs):

        self._app_ctx = app_ctx(source_id, app_service_type, apps_config_data)
        self._source_id = source_id
        self._parameters = self._app_ctx.load_app_parameters()

        self._client = client(val=val, **self._app_ctx.load_app_service_config(), **kwargs)

        self._return_data_only = self._parameters.get('return_data_only', False)
        self._routing_separator = self._parameters.get('routing_separator', "/")

        self._assert_helper = LoggedAssertHelper()
        self._request = None

    @property
    def parameters(self) -> dict:
        return self._parameters

    @property
    def source_id(self) -> str:
        return self._source_id

    @property
    def verify(self) -> LoggedAssertHelper:
        return self._assert_helper

    @property
    def request(self) -> IWebRequestBuilder:
        if self._request is None:
            self._request = self.get_request_builder()
        return self._request

    @property
    def client(self) -> IWebClient:
        return self._client

    def send_request(self, r: IWebServiceRequest, **kwargs) -> IResponse[T]:
        return self._client.execute_request(r, self.response_type, **kwargs)

    def get_request_builder(self) -> IWebRequestBuilder:
        return RequestBuilder(self._routing_separator)

    def initialize(self) -> (IWebRequestBuilder, IWebClient):
        return self.request, self.client

    def set_session_data(self, **kwargs):
       ...
