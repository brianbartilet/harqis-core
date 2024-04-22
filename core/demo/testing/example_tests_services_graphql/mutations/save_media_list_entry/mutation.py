import os
from core.web.services.fixtures.graphql import BaseFixtureServiceGraphQL


class ServiceMutationSaveMediaListEntry(BaseFixtureServiceGraphQL):
    def __init__(self, config, gql_file: str = 'save_media_list_entry.tpl.gql', **kwargs):
        self.path = os.path.dirname(os.path.abspath(__file__))
        super(ServiceMutationSaveMediaListEntry, self)\
            .__init__(config, gql_file=gql_file, base_path=self.path, **kwargs)

    def test_mutation_save_media_with_test_case_data(self, sample_variables: dict):
        self.request.set_variables(sample_variables)
        return self.client.execute_request(self.request.build())