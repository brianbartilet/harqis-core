from core.web.services.core.constants.http_methods import HttpMethod

from demo.testing.__tpl_tests_services_rest.services.base_service import BaseServiceApp
from demo.testing.__tpl_tests_services_rest.dto.user import DtoUser
from demo.testing.__tpl_tests_services_rest.dto.payload import DtoPostPayload


class ServiceRestExamplePost(BaseServiceApp):

    def __init__(self, config, **kwargs):
        super(ServiceRestExamplePost, self).__init__(config, **kwargs)
        self.request.add_uri_parameter('posts')

    def request_get(self):
        self.request\
            .set_method(HttpMethod.GET)\
            .add_uri_parameter('1')

        return self.client.execute_request(self.request.build(), response_hook=DtoUser)

    def request_post(self, payload: DtoPostPayload):
        self.request \
            .set_method(HttpMethod.POST) \
            .add_json_body(payload)

        return self.client.execute_request(self.request.build())

    def request_delete(self):
        self.request \
            .set_method(HttpMethod.DELETE)

        return self.request.build()