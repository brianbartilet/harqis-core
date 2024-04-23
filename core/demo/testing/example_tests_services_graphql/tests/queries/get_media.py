import pytest

from http import HTTPStatus

from demo.testing.example_tests_services_graphql.config import CONFIG
from demo.testing.example_tests_services_graphql.queries.get_media.query import ServiceQueryGetMedia


@pytest.fixture()
def given():
    """
    Pytest fixture that sets up the query service and test payload for media retrieval.

    This fixture initializes the ServiceQueryGetMedia with a given configuration and
    constructs a payload necessary for the test. The payload and service instance are
    used in tests that query media data, specifically for media type "ANIME".

    Returns:
        tuple: Contains the ServiceQueryGetMedia instance and the test payload dictionary.
    """
    given_query = ServiceQueryGetMedia(CONFIG)
    given_payload = {'id': 1, 'type': "ANIME"}

    return given_query, given_payload


@pytest.mark.sanity  # Mark the test as a sanity test
def test_get_query_media_with_test_case_data(given):
    """
    Tests the retrieval of media data using a GraphQL query with predefined test case data.

    This test validates the media query operation by ensuring that the response is
    successful and contains the expected 'Media' key. It specifically checks the behavior
    when querying for media type "ANIME".

    Args:
        given (tuple): Fixture that provides the ServiceQueryGetMedia instance and payload.

    Asserts:
        Asserts that the response status code is HTTPStatus.OK, indicating a successful query.
        Asserts that the response data includes the 'Media' key, ensuring the media data is retrieved.
    """
    given_query, given_payload = given
    when_response = given_query.get_query_media_with_test_case_data(given_payload)
    then = given_query.verify.common
    then.assert_that(when_response.status_code, then.equal_to(HTTPStatus.OK))
    then.assert_that(when_response.data, then.has_key('Media'))
