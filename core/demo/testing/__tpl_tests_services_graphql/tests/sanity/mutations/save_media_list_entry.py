import pytest
from http import HTTPStatus

from demo.testing.__tpl_tests_services_graphql.config import CONFIG
from demo.testing.__tpl_tests_services_graphql.mutations.save_media_list_entry.mutation import ServiceMutationSaveMediaListEntry


@pytest.fixture()
def set_up():
    given_mutation = ServiceMutationSaveMediaListEntry(CONFIG)
    given_payload = {'id': 26, 'mediaId': 8, 'status': "REPEATING"}

    return given_mutation, given_payload


def test_mutation_save_media_with_test_case_data(set_up):
    given_mutation, given_payload = set_up

    when_response = given_mutation.test_mutation_save_media_with_test_case_data(given_payload)
    then = given_mutation.verify.common
    then.assert_that(when_response.status_code, then.equal_to(HTTPStatus.BAD_REQUEST))

    then.assert_that(when_response.data, then.has_key('SaveMediaListEntry'))
    then.assert_that(True, when_response.data['SaveMediaListEntry'] is None)