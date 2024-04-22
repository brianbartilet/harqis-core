import pytest

from http import HTTPStatus

from demo.testing.example_tests_services_rest.services.posts.post import ServiceRestExamplePost
from demo.testing.example_tests_services_rest.config import CONFIG
from demo.testing.example_tests_services_rest.models.user import User
from demo.testing.example_tests_services_rest.models.payload import PostPayload


@pytest.fixture()
def given_service():
    given_service = ServiceRestExamplePost(CONFIG)

    return given_service


@pytest.mark.sanity
def test_run_unit_tests_get(given_service):
    when = given_service.request_get()
    then = given_service.verify.common
    then.assert_that(when.status_code, then.equal_to(HTTPStatus.OK))
    then.assert_that(isinstance(when.data, User), True)


@pytest.mark.sanity
def test_run_unit_tests_post(given_service):
    payload = {
        'title': 'Test Post',
        'body': 'This is a test post.',
        'userId': 1
    }

    given_payload = PostPayload(**payload)
    when = given_service.request_post(given_payload)
    then = given_service.verify.common
    then.assert_that(when.status_code, then.equal_to(HTTPStatus.CREATED))
    then.assert_that(when.data, then.has_entries())


@pytest.mark.sanity
def test_run_unit_tests_delete(given_service):
    given_request = given_service.request_delete()
    when = given_service.send_request(given_request)
    then = given_service.verify.common
    then.assert_that(when.status_code, then.equal_to(HTTPStatus.NOT_FOUND))



