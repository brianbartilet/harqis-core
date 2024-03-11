import unittest

from utilities import *
from web.services import *
from web.services.core.response import deserialized
from web.services.core.config.webservice import AppConfigWSClient

response_check_get = {
    "userId": 1,
    "id": 1,
    "title": "sunt aut facere repellat provident occaecati excepturi optio reprehenderit",
    "body": "quia et suscipit\nsuscipit recusandae consequuntur expedita et cum\nreprehenderit molestiae ut ut quas totam\nnostrum rerum est autem sunt rem eveniet architecto"
}

post_payload = {
    'title': 'Test Post',
    'body': 'This is a test post.',
    'userId': 1
}

test_config = AppConfigWSClient(
    app_id='TEST APPLICATION',
    client='rest',
    parameters={
        "base_url": "https://jsonplaceholder.typicode.com/",
        "response_encoding": "utf-8",
        "verify_ssh": False
    }
)


class TestsUnitWebServices(unittest.TestCase):
    def test_run_unit_tests_get(self):
        child_resource = ChildTestFixtureResource()
        child_resource_response = child_resource.get()
        assert_that(child_resource_response.status_code, equal_to(HTTPStatus.OK))
        assert_that(child_resource_response.json_data, equal_to(response_check_get))

    def test_run_unit_tests_post(self):
        child_resource = ChildTestFixtureResource()
        child_resource_response = child_resource.post()
        assert_that(child_resource_response.status_code, equal_to(HTTPStatus.CREATED))
        assert_that(child_resource_response.json_data, has_entries(post_payload))

    def test_run_unit_tests_delete(self):
        child_resource = ChildTestFixtureResource()
        child_resource_response = child_resource.delete()
        assert_that(child_resource_response.status_code, equal_to(HTTPStatus.NOT_FOUND))


class BaseTestFixtureApp(FixtureRest):
    def __init__(self):
        super(BaseTestFixtureApp, self).__init__(config=test_config)


class ChildTestFixtureResource(BaseTestFixtureApp):
    @deserialized(dict)
    def get(self):
        self.request\
            .set_method(HttpMethod.GET)\
            .add_uri_parameter('posts')\
            .add_uri_parameter('1')

        return self.send_request(self.request.build())

    @deserialized(dict)
    def post(self):
        self.request \
            .set_method(HttpMethod.POST) \
            .add_uri_parameter('posts')\
            .add_json_payload(post_payload)

        return self.send_request(self.request.build())

    @deserialized(dict)
    def delete(self):
        self.request \
            .set_method(HttpMethod.DELETE) \
            .add_uri_parameter('posts')

        return self.send_request(self.request.build())
