import os

from web.services.fixtures.graphql import BaseFixtureServiceGraphQL


class BaseTestFixtureAppQuery(BaseFixtureServiceGraphQL):
    def __init__(self, config, gql_file: str = 'query.tpl.gql'):
        super(BaseTestFixtureAppQuery, self)\
            .__init__(config, gql_file=gql_file, base_path=os.path.join(os.getcwd(), 'graphql'))

    def get_sample_request(self, sample_variables: dict):
        self.request.set_variables(sample_variables)
        return self.request.build()



