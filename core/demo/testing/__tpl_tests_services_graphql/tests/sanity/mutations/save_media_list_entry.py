import unittest

from http import HTTPStatus

from demo.testing.__tpl_tests_services_graphql.config import CONFIG
from demo.testing.__tpl_tests_services_graphql.mutations.save_media_list_entry.mutation \
    import ServiceMutationSaveMediaListEntry


class TestsUnitWebServices(unittest.TestCase):
    def setUp(self):
        self.given_mutation = ServiceMutationSaveMediaListEntry(CONFIG)
        self.given_payload = {'id': 26, 'mediaId': 8, 'status': "REPEATING" }

    def test_mutation_save_media_with_test_case_data(self):
        when_response = self.given_mutation.test_mutation_save_media_with_test_case_data(self.given_payload)
        then = self.given_mutation.verify.common
        then.assert_that(when_response.status_code, then.equal_to(HTTPStatus.BAD_REQUEST))

        then.assert_that(when_response.data, then.has_key('SaveMediaListEntry'))
        self.assertTrue(when_response.data['SaveMediaListEntry'] is None)
