import os
from web.services.fixtures.graphql import BaseFixtureServiceGraphQL


class BaseTestFixtureAppMutation(BaseFixtureServiceGraphQL):
    def __init__(self, config, gql_file: str = 'mutation.tpl.gql'):
        super(BaseTestFixtureAppMutation, self)\
            .__init__(config, gql_file=gql_file, base_path=os.path.join(os.getcwd(), 'graphql'))
