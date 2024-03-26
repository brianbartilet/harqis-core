import pytest

from http import HTTPStatus

from demo.testing.__tpl_tests_services_graphql.config import CONFIG
from demo.testing.__tpl_tests_services_graphql.queries.get_media.query import ServiceQueryGetMedia


@pytest.fixture()
def given():
    given_query = ServiceQueryGetMedia(CONFIG)
    given_payload = {'id': 1, 'type': "ANIME"}

    return given_query, given_payload


def test_get_query_media_with_test_case_data(given):
    given_query, given_payload = given
    when_response = given_query.get_query_media_with_test_case_data(given_payload)
    then = given_query.verify.common
    then.assert_that(when_response.status_code, then.equal_to(HTTPStatus.OK))
    then.assert_that(when_response.data, then.has_key('Media'))
