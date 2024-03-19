import unittest

from http import HTTPStatus
from web.services.tests.graphql.sample_query import BaseTestFixtureAppQuery

from web.services.core.config.webservice import AppConfigWSClient
from web.services.core.json import JsonObject

# this would be the configuration for the application would be loaded externally
given_config = AppConfigWSClient(
    client='graphql',
    parameters={
        "base_url": "https://graphql.anilist.co/",
        "response_encoding": "utf-8",
        "verify": True
    }
)


class TestDtoQuery(JsonObject):
    id: int = None
    type: str = None


class TestsUnitWebServices(unittest.TestCase):

    def test_sample_query(self):
        given_fixture = BaseTestFixtureAppQuery(given_config)
        given_payload = {'id': 1, 'type': "ANIME" }
        given_request = given_fixture.get_sample_request(given_payload)

        when = given_fixture.send_request(given_request)

        then = given_fixture.verify.common
        then.assert_that(when.status_code, then.equal_to(HTTPStatus.OK))
        then.assert_that(when.data, then.has_key('Media'))

    def test_sample_query_with_type(self):
        given_fixture = BaseTestFixtureAppQuery(given_config)
        given_payload = {'id': 1, 'type': "ANIME" }
        given_request = given_fixture.get_sample_request(given_payload)

        when = given_fixture.send_request(given_request, response_hook=TestDtoQuery)

        then = given_fixture.verify.common
        then.assert_that(when.status_code, then.equal_to(HTTPStatus.OK))
        then.assert_that(when.data, then.has_property('Media'))

        #  test chaining
        when = given_fixture.send_request(given_request, response_hook=TestDtoQuery)
        then.assert_that(when.status_code, then.equal_to(HTTPStatus.OK))

    def test_sample_query_with_invalid_gql(self):
        given_fixture = BaseTestFixtureAppQuery(given_config, gql_file='invalid.tpl.gql')
        given_payload = {'invalid_key': 0 }
        given_request = given_fixture.get_sample_request(given_payload)
        when = given_fixture.send_request(given_request)
        when_errors = given_fixture.client.get_errors()

        then = given_fixture.verify.common
        then.assert_that(when.status_code, then.equal_to(HTTPStatus.BAD_REQUEST))
        then.assert_that(isinstance(when_errors.data, list), True)