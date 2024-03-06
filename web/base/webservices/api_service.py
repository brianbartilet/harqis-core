import functools
import time
from typing import TypeVar, Type

from web.base.webservices.webservice_client import BaseApiClient

from web.core.services.business import *
from web.core.services.contracts import *

from utilities.logged_assert_helper import LoggedAssertHelper
from utilities.object_utils import ObjectUtil
from utilities.custom_logger import custom_logger
from utilities.apps_context import AppConfigurationContext


log = custom_logger()


T = TypeVar("T")
V = TypeVar("V")


def deserialized(type_hook: Type[T] = BaseDto, child: str = None, wait=None):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(self, *args, **kwargs):
            self.initialize()
            self.response_type = type_hook

            if wait is not None:
                time.sleep(wait)

            response = func(self, *args, **kwargs)

            if self._return_data_only:
                try:

                    if child is not None:
                        if isinstance(type_hook(), dict):
                            return ObjectUtil.convert_obj_to_sc(response.json_data[child])
                        else:
                            return ObjectUtil.convert_obj_to_sc(eval("response.deserialized_data." + child))
                    else:
                        return ObjectUtil.convert_obj_to_sc(response.json_data)

                except Exception as e:
                    log.warning("Cannot access deserialized data. Returning full response. ERROR: {0}".format(e))
                    return response

            else:
                return response

        return wrapper

    return decorator


class ApiService(IApiService[T]):

    response_type = Type[T]
    headers = HttpHeaders

    def __init__(self,
                 source_id: str,
                 apps_config_data: dict,
                 client: type = BaseApiClient,
                 val: Type[T] = BaseDto,
                 app_ctx: type = AppConfigurationContext,
                 app_service_type: ServiceClientType = ServiceClientType.WEBSERVICE,
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
    def request(self) -> IApiRequestBuilder:
        if self._request is None:
            self._request = self.get_request_builder()
        return self._request

    @property
    def client(self) -> IApiClient:
        return self._client

    def send_get_request(self, request: IApiRequest, **kwargs) -> IApiResponse[T]:
        request.set_request_type(Method.GET)
        return self._client.execute(request, self.response_type, **kwargs)

    def send_post_request(self, request: IApiRequest, **kwargs) -> IApiResponse[T]:
        request.set_request_type(Method.POST)
        return self._client.execute(request, self.response_type, **kwargs)

    def send_delete_request(self, request: IApiRequest, **kwargs) -> IApiResponse[T]:
        request.set_request_type(Method.DELETE)
        return self._client.execute(request, self.response_type, **kwargs)

    def send_put_request(self, request: IApiRequest, **kwargs) -> IApiResponse[T]:
        request.set_request_type(Method.PUT)
        return self._client.execute(request, self.response_type, **kwargs)

    def send_patch_request(self, request: IApiRequest, **kwargs) -> IApiResponse[T]:
        request.set_request_type(Method.PATCH)
        return self._client.execute(request, self.response_type, **kwargs)

    def get_request_builder(self) -> IApiRequestBuilder:
        return RequestBuilder(self._routing_separator)

    def initialize(self) -> (IApiRequestBuilder, IApiClient):
        return self.request, self.client

    def set_session_data(self, **kwargs):
       ...
