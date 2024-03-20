from core.web.services.fixtures.rest import BaseFixtureServiceRest
from core.web.services.core.config.webservice import AppConfigWSClient

# this would be the configuration for the application would be loaded externally
test_config = AppConfigWSClient(
    client='rest',
    parameters={
        "base_url": "https://jsonplaceholder.typicode.com/",
        "response_encoding": "utf-8",
        "verify": True
    }
)


class BaseTestFixtureService(BaseFixtureServiceRest):
    def __init__(self):
        super(BaseTestFixtureService, self).__init__(config=test_config)
