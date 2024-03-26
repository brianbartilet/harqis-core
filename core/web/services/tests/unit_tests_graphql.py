import unittest
import os

from http import HTTPStatus
from core.web.services.tests.graphql.sample_query import BaseTestFixtureAppQuery

from core.web.services.core.config.webservice import AppConfigWSClient
from core.web.services.core.json import JsonObject

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
    def setUp(self):
        self.path = os.path.dirname(os.path.abspath(__file__))
        self.given_fixture = BaseTestFixtureAppQuery(given_config, base_path=os.path.join(self.path, 'graphql'))

    def test_sample_query(self):

        given_payload = {'id': 1, 'type': "ANIME"}
        given_request = self.given_fixture.get_sample_request(given_payload)

        when = self.given_fixture.send_request(given_request)

        then = self.given_fixture.verify.common
        then.assert_that(when.status_code, then.equal_to(HTTPStatus.OK))
        then.assert_that(when.data, then.has_key('Media'))

    def test_sample_query_with_type(self):
        given_payload = {'id': 1, 'type': "ANIME"}
        given_request = self.given_fixture.get_sample_request(given_payload)

        when = self.given_fixture.send_request(given_request, response_hook=TestDtoQuery)

        then = self.given_fixture.verify.common
        then.assert_that(when.status_code, then.equal_to(HTTPStatus.OK))
        then.assert_that(when.data, then.has_property('Media'))

        #  test chaining
        when = self.given_fixture.send_request(given_request, response_hook=TestDtoQuery)
        then.assert_that(when.status_code, then.equal_to(HTTPStatus.OK))

    def test_sample_query_with_invalid_gql(self):
        with self.assertRaises(FileNotFoundError):
            given_fixture = BaseTestFixtureAppQuery(given_config, gql_file='invalid.tpl.gql', base_path=self.path)
            given_payload = {'invalid_key': 0}
            given_fixture.get_sample_request(given_payload)
