import unittest

from http import HTTPStatus

from demo.testing.__template_tests_services_graphql.config import CONFIG
from demo.testing.__template_tests_services_graphql.queries.get_media.query import ServiceQueryGetMedia


class TestsUnitWebServices(unittest.TestCase):
    def setUp(self):
        self.given_query = ServiceQueryGetMedia(CONFIG)
        self.given_payload = {'id': 1, 'type': "ANIME" }

    def test_get_query_media_with_test_case_data(self):
        when_response = self.given_query.get_query_media_with_test_case_data(self.given_payload)
        then = self.given_query.verify.common
        then.assert_that(when_response.status_code, then.equal_to(HTTPStatus.OK))
        then.assert_that(when_response.data, then.has_key('Media'))
