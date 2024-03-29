import pytest

from http import HTTPStatus

from demo.testing.__tpl_tests_services_rest.services.posts.post import ServiceRestExamplePost
from demo.testing.__tpl_tests_services_rest.config import CONFIG
from demo.testing.__tpl_tests_services_rest.models.user import User
from demo.testing.__tpl_tests_services_rest.models.payload import PostPayload


@pytest.fixture()
def given():
    given = ServiceRestExamplePost(CONFIG)

    given_payload = {
        'title': 'Test Post',
        'body': 'This is a test post.',
        'userId': 1
    }
    return given, given_payload


@pytest.mark.sanity
def test_run_unit_tests_get(given):
    given, given_payload = given
    when = given.request_get()
    then = given.verify.common
    then.assert_that(when.status_code, then.equal_to(HTTPStatus.OK))
    then.assert_that(isinstance(when.data, User), True)


@pytest.mark.sanity
def test_run_unit_tests_post(given):
    given, given_payload = given
    given_payload_ = PostPayload(**given_payload)
    when = given.request_post(given_payload_)
    then = given.verify.common
    then.assert_that(when.status_code, then.equal_to(HTTPStatus.CREATED))
    then.assert_that(when.data, then.has_entries())


@pytest.mark.sanity
def test_run_unit_tests_delete(given):
    given, given_payload = given
    given_request = given.request_delete()
    when = given.send_request(given_request)
    then = given.verify.common
    then.assert_that(when.status_code, then.equal_to(HTTPStatus.NOT_FOUND))



