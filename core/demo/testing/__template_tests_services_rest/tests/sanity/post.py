import unittest

from http import HTTPStatus

from demo.testing.__template_tests_services_rest.services.posts.post import ServiceRestExamplePost
from demo.testing.__template_tests_services_rest.config import CONFIG
from demo.testing.__template_tests_services_rest.dto.user import DtoUser
from demo.testing.__template_tests_services_rest.dto.payload import DtoPostPayload


class TestsUnitWebServices(unittest.TestCase):
    def setUp(self):
        self.given = ServiceRestExamplePost(CONFIG)

        self.post_payload = {
            'title': 'Test Post',
            'body': 'This is a test post.',
            'userId': 1
        }

    def test_run_unit_tests_get(self):
        when = self.given.request_get()
        then = self.given.verify.common
        then.assert_that(when.status_code, then.equal_to(HTTPStatus.OK))
        then.assert_that(isinstance(when.data, DtoUser), True)

    def test_run_unit_tests_post(self):
        given_payload = DtoPostPayload(**self.post_payload)
        when = self.given.request_post(given_payload)
        then = self.given.verify.common
        then.assert_that(when.status_code, then.equal_to(HTTPStatus.CREATED))
        then.assert_that(when.data, then.has_entries())

    def test_run_unit_tests_delete(self):
        given_request = self.given.request_delete()
        when = self.given.send_request(given_request)
        then = self.given.verify.common
        then.assert_that(when.status_code, then.equal_to(HTTPStatus.NOT_FOUND))



