from core.web.services.fixtures.rest import BaseFixtureServiceRest
from core.web.services.core.constants.http_headers import HttpHeaders


class BaseServiceElastic(BaseFixtureServiceRest):

    def __init__(self, config, **kwargs):
        super(BaseServiceElastic, self).__init__(config, **kwargs)
        api_key = self.config.app_data["api_key"]
        self.request\
            .add_header(HttpHeaders.AUTHORIZATION, f'Bearer {api_key}')
