from web.services.core.constants.http_methods import HttpMethod
from web.services.core.json import JsonObject

from .base_resource import BaseTestFixtureApp

response_check_get = {"userId": 1,
                      "id": 1,
                      "title": "sunt aut facere repellat provident occaecati excepturi optio reprehenderit",
                      "body": "quia et suscipit\nsuscipit recusandae consequuntur expedita "
                              "et cum\nreprehenderit molestiae ut ut quas totam\nnostrum rerum "
                              "est autem sunt rem eveniet architecto"}

post_payload = {
    'title': 'Test Post',
    'body': 'This is a test post.',
    'userId': 1
}


class DtoUserTest(JsonObject):
    user_id: int = None
    id: int = None
    title: str = None
    body: str = None


class DtoUserTestCamel(JsonObject):
    userId: int = None
    title: str = None
    body: str = None


class ChildTestFixtureResource(BaseTestFixtureApp):

    def get(self):
        self.request\
            .set_method(HttpMethod.GET)\
            .add_uri_parameter('posts')\
            .add_uri_parameter('1')

        return self.request.build()

    def post(self):
        self.request \
            .set_method(HttpMethod.POST) \
            .add_uri_parameter('posts')\
            .add_json_payload(post_payload)

        return self.request.build()

    def post_with_json_object(self, payload: JsonObject):
        self.request \
            .set_method(HttpMethod.POST) \
            .add_uri_parameter('posts')\
            .add_json_body(payload)

        return self.request.build()

    def delete(self):
        self.request \
            .set_method(HttpMethod.DELETE) \
            .add_uri_parameter('posts')

        return self.request.build()
