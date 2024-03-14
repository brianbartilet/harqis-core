from web.services.fixtures.graphql import BaseFixtureGraphQL
from web.services.core.config.webservice import AppConfigWSClient
from web.services.core.json import JsonObject

# this would be the configuration for the application would be loaded externally
test_config = AppConfigWSClient(app_id='TEST GRAPHQL QUERY', client='graphql', parameters={
        "base_url": "https://graphql.anilist.co/",
        "response_encoding": "utf-8",
        "verify": True
    })


class TestDtoQuery(JsonObject):
    id: int
    type: str


class BaseTestFixtureAppQuery(BaseFixtureGraphQL):
    def __init__(self, gql_file: str = 'query.tpl.gql'):
        super(BaseTestFixtureAppQuery, self).__init__(config=test_config, gql_file=gql_file, base_path='graphql')

    def sample_request(self, sample_variables: dict):
        self.request.set_variables(sample_variables)
        return self.request.build()



