import unittest

from http import HTTPStatus

from web.services.tests.rest.child_resource \
    import ChildTestFixtureResource, DtoUserTest, DtoUserTestCamel, post_payload, response_check_get


class TestsUnitWebServices(unittest.TestCase):
    def setUp(self):
        self.given = ChildTestFixtureResource()

    def test_run_unit_tests_get(self):
        given_request = self.given.request_get()
        when = self.given.send_request(given_request)
        then = self.given.verify.common
        then.assert_that(when.status_code, then.equal_to(HTTPStatus.OK))
        then.assert_that(when.data, then.equal_to(response_check_get))

    def test_run_unit_tests_get_typed(self):
        given_request = self.given.request_get()
        when = self.given.send_request(given_request, response_hook=DtoUserTest)
        then = self.given.verify.common
        then.assert_that(when.status_code, then.equal_to(HTTPStatus.OK))
        then.assert_that(isinstance(when.data, DtoUserTest), True)

    def test_run_unit_tests_get_response(self):
        when = self.given.get_request_no_hook()
        then = self.given.verify.common
        then.assert_that(when.status_code, then.equal_to(HTTPStatus.OK))
        then.assert_that(when.data, then.equal_to(response_check_get))

    def test_run_unit_tests_get_typed_response(self):
        when = self.given.get_request_with_hook()
        then = self.given.verify.common
        then.assert_that(when.status_code, then.equal_to(HTTPStatus.OK))
        then.assert_that(isinstance(when.data, DtoUserTest), True)

    def test_run_unit_tests_post(self):
        given_request = self.given.request_post()
        when = self.given.send_request(given_request)
        then = self.given.verify.common
        then.assert_that(when.status_code, then.equal_to(HTTPStatus.CREATED))
        then.assert_that(when.data, then.has_entries(post_payload))

        #  test succeeding calls
        when = self.given.send_request(given_request)
        then = self.given.verify.common
        then.assert_that(when.status_code, then.equal_to(HTTPStatus.CREATED))
        then.assert_that(when.data, then.has_entries(post_payload))

    def test_run_unit_tests_post_with_object(self):
        given_payload = DtoUserTest(**post_payload)

        given_request = self.given.request_post_with_json_object(given_payload)
        when = self.given.send_request(given_request)
        then = self.given.verify.common
        then.assert_that(when.status_code, then.equal_to(HTTPStatus.CREATED))

    def test_run_unit_tests_post_with_object_camel(self):
        given_payload = DtoUserTestCamel(**post_payload)

        given_request = self.given.request_post_with_json_object(given_payload)
        when = self.given.send_request(given_request)
        then = self.given.verify.common
        then.assert_that(when.status_code, then.equal_to(HTTPStatus.CREATED))

    def test_run_unit_tests_delete(self):
        given_request = self.given.request_delete()
        when = self.given.send_request(given_request)
        then = self.given.verify.common
        then.assert_that(when.status_code, then.equal_to(HTTPStatus.NOT_FOUND))
