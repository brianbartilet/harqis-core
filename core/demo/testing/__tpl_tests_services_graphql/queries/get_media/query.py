import os
from core.web.services.fixtures.graphql import BaseFixtureServiceGraphQL
from demo.testing.__tpl_tests_services_graphql.queries.get_media.models.media import Media


class ServiceQueryGetMedia(BaseFixtureServiceGraphQL):
    def __init__(self, config, gql_file='get_media.tpl.gql', **kwargs):
        self.path = os.path.dirname(os.path.abspath(__file__))
        super(ServiceQueryGetMedia, self)\
            .__init__(config, gql_file=gql_file, base_path=self.path, **kwargs)

    def get_query_media_with_test_case_data(self, sample_variables: dict):
        self.request.set_variables(sample_variables)
        return self.client.execute_request(self.request.build())

    def get_query_media_with_test_response_hook(self, sample_variables: dict):
        self.request.set_variables(sample_variables)
        return self.client.execute_request(self.request.build(), response_hook=Media)



