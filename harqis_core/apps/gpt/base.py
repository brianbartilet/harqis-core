from openai import OpenAI

from web.services.fixtures.rest import BaseFixtureServiceRest
from web.services.core.constants.http_headers import HttpHeaders


class BaseServiceHarqisGPT(BaseFixtureServiceRest):

    def __init__(self, config, **kwargs):
        super(BaseServiceHarqisGPT, self).__init__(config, **kwargs)
        self.request\
            .add_header(HttpHeaders.AUTHORIZATION, f'Bearer {self.config.app_data["api_key"]}')


