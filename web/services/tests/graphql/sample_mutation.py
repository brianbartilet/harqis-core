from web.services import *

# this would be the configuration for the application would be loaded externally
test_config = AppConfigWSClient(app_id='TEST GRAPHQL MUTATION', client='graphql', parameters={
        "base_url": "https://graphql.anilist.co/",
        "response_encoding": "utf-8",
        "verify": True
    })


class BaseTestFixtureAppQuery(BaseFixtureGraphQL):
    def __init__(self):
        super(BaseTestFixtureAppQuery, self).__init__(config=test_config, gql_file='mutation.tpl.gql')
