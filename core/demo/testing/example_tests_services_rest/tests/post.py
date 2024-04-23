import pytest

from http import HTTPStatus

from demo.testing.example_tests_services_rest.services.posts.post import ServiceRestExamplePost
from demo.testing.example_tests_services_rest.config import CONFIG
from demo.testing.example_tests_services_rest.models.user import User
from demo.testing.example_tests_services_rest.models.payload import PostPayload


@pytest.fixture()
def given_service():
    """
    A pytest fixture that provides a service instance configured for testing.

    Returns:
        ServiceRestExamplePost: An instance of ServiceRestExamplePost initialized with configuration.
    """
    given_service = ServiceRestExamplePost(CONFIG)
    return given_service


@pytest.mark.sanity
def test_run_unit_tests_get(given_service):
    """
    Test the GET request functionality to verify if it successfully retrieves a post and returns HTTPStatus.OK.

    Args:
        given_service (ServiceRestExamplePost): The service instance to use for making the GET request.
    """
    when = given_service.request_get()
    then = given_service.verify.common
    then.assert_that(when.status_code, then.equal_to(HTTPStatus.OK))
    then.assert_that(isinstance(when.data, dict), True)


@pytest.mark.sanity
def test_run_unit_tests_post(given_service):
    """
    Test the POST request functionality by sending a predefined payload and verifying the creation status code.

    Args:
        given_service (ServiceRestExamplePost): The service instance to use for making the POST request.
    """
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
def test_run_unit_tests_get_with_hook(given_service):
    """
    GET request functionality with a response hook, check that the data returned is correctly parsed into a User model.

    Args:
        given_service (ServiceRestExamplePost): The service instance to use for the GET request with a response hook.
    """
    when = given_service.request_get_with_hook()
    then = given_service.verify.common
    then.assert_that(isinstance(when.data, User), True)


