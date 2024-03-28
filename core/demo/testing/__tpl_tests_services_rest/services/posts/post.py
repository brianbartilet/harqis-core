from core.web.services.core.constants.http_methods import HttpMethod

from demo.testing.__tpl_tests_services_rest.services.base_service import BaseServiceApp
from demo.testing.__tpl_tests_services_rest.models.user import User
from demo.testing.__tpl_tests_services_rest.models.payload import PostPayload


class ServiceRestExamplePost(BaseServiceApp):

    def __init__(self, config, **kwargs):
        super(ServiceRestExamplePost, self).__init__(config, **kwargs)
        self.request.add_uri_parameter('posts')

    def request_get(self):
        self.request\
            .set_method(HttpMethod.GET)\
            .add_uri_parameter('1')

        return self.client.execute_request(self.request.build(), response_hook=User)

    def request_post(self, payload: PostPayload):
        self.request \
            .set_method(HttpMethod.POST) \
            .add_json_body(payload)

        return self.client.execute_request(self.request.build())

    def request_delete(self):
        self.request \
            .set_method(HttpMethod.DELETE)

        return self.request.build()