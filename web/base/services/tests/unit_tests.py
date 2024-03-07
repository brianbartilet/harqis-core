import unittest

from utilities import *
from web.base.services import *


BASE_TEST_CONFIG = 'NEW_APP'
apps_config = {
    BASE_TEST_CONFIG: {
            "client": {
                "base_url": "https://jsonplaceholder.typicode.com/",
                "response_encoding": "utf-8",
                "verify": False
            },
            "parameters":{
            }
    }
}

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

class BaseApiServiceTestApp(ApiService, Generic[T]):

    def __init__(self, source_id, **kwargs):
        super(BaseApiServiceTestApp, self)\
            .__init__(source_id=source_id,
                      apps_config_data=apps_config,
                      **kwargs)

class ChildApiServiceTestApp(BaseApiServiceTestApp):
    @deserialized(dict)
    def get(self):
        self.request\
            .add_uri_parameter('posts')\
            .add_uri_parameter('1')

        return self.send_get_request(self.request.build())

    @deserialized(dict)
    def post(self):
        self.request\
            .add_uri_parameter('posts')\
            .add_json_payload(post_payload)

        return self.send_post_request(self.request.build())

class TestsUnitWebServices(unittest.TestCase):
    def test_run_unit_tests_get(self):
        service = ChildApiServiceTestApp(source_id=BASE_TEST_CONFIG)
        response = service.get()
        assert_that(response.status_code, equal_to(200))
        assert_that(response.json_data, equal_to(response_check_get))

    def test_run_unit_tests_post(self):
        service = ChildApiServiceTestApp(source_id=BASE_TEST_CONFIG)
        response = service.post()
        assert_that(response.status_code, equal_to(201))
        assert_that(response.json_data, has_entries(post_payload))


