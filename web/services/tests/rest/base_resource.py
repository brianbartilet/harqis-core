from web.services.fixtures.rest import BaseFixtureRest
from web.services.core.config.webservice import AppConfigWSClient

# this would be the configuration for the application would be loaded externally
test_config = AppConfigWSClient(app_id='TEST REST', client='rest', parameters={
        "base_url": "https://jsonplaceholder.typicode.com/",
        "response_encoding": "utf-8",
        "verify": True
    })


class BaseTestFixtureApp(BaseFixtureRest):
    def __init__(self):
        super(BaseTestFixtureApp, self).__init__(config=test_config)
