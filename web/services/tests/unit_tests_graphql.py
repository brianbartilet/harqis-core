import unittest

from http import HTTPStatus
from web.services.tests.graphql.sample_query import BaseTestFixtureAppQuery, TestDtoQuery


class TestsUnitWebServices(unittest.TestCase):

    def test_sample_query(self):
        given_fixture = BaseTestFixtureAppQuery()
        variables = {'id': 1, 'type': "ANIME" }
        given_request = given_fixture.sample_request(variables)

        when = given_fixture.send_request(given_request)

        then = given_fixture.verify.common
        then.assert_that(when.status_code, then.equal_to(HTTPStatus.OK))
        then.assert_that(when.data, then.has_key('Media'))

    def test_sample_query_with_type(self):
        given_fixture = BaseTestFixtureAppQuery()
        variables = {'id': 1, 'type': "ANIME" }
        given_request = given_fixture.sample_request(variables)

        when = given_fixture.send_request(given_request, response_hook=TestDtoQuery)

        then = given_fixture.verify.common
        then.assert_that(when.status_code, then.equal_to(HTTPStatus.OK))
        then.assert_that(when.data, then.has_property('Media'))

    def test_sample_query_with_invalid_gql(self):
        given_fixture = BaseTestFixtureAppQuery(gql_file='invalid.tpl.gql')
        variables = {'invalid_key': 0 }
        given_request = given_fixture.sample_request(variables)
        when = given_fixture.send_request(given_request)
        when_errors = given_fixture.client.get_errors()

        then = given_fixture.verify.common
        then.assert_that(when.status_code, then.equal_to(HTTPStatus.BAD_REQUEST))
        then.assert_that(isinstance(when_errors.data, list), True)