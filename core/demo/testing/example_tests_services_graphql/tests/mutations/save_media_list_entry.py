import pytest
from http import HTTPStatus

from demo.testing.example_tests_services_graphql.config import CONFIG
from demo.testing.example_tests_services_graphql.mutations.save_media_list_entry.mutation import ServiceMutationSaveMediaListEntry


@pytest.fixture()
def set_up():
    """
    Pytest fixture to set up the conditions before running tests.

    This fixture initializes a ServiceMutationSaveMediaListEntry instance with a configuration and
    a predefined payload. It is used in tests to prepare the necessary objects and data.

    Returns:
        tuple: A tuple containing the ServiceMutationSaveMediaListEntry instance and the payload dictionary.
    """
    given_mutation = ServiceMutationSaveMediaListEntry(CONFIG)
    given_payload = {'id': 26, 'mediaId': 8, 'status': "REPEATING"}

    return given_mutation, given_payload


@pytest.mark.sanity  # Mark the test as a sanity test
def test_mutation_save_media_with_test_case_data(set_up):
    """
    Tests the mutation to save a media list entry using provided test case data.

    This test checks that the response to saving a media list entry behaves as expected under the conditions
    defined in the payload. Specifically, it verifies that the correct status code and response data are returned.

    Args:
        set_up (tuple): Fixture that provides the ServiceMutationSaveMediaListEntry instance and payload.

    Asserts:
        Asserts that the status code of the response is HTTPStatus.BAD_REQUEST, indicating an error in input.
        Asserts that the 'SaveMediaListEntry' key exists in the response data and that its value is None, as expected for this test case.
    """
    given_mutation, given_payload = set_up

    when_response = given_mutation.test_mutation_save_media_with_test_case_data(given_payload)
    then = given_mutation.verify.common
    then.assert_that(when_response.status_code, then.equal_to(HTTPStatus.BAD_REQUEST))

    then.assert_that(when_response.data, then.has_key('SaveMediaListEntry'))
    then.assert_that(True, when_response.data['SaveMediaListEntry'] is None)