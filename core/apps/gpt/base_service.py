from core.web.services.fixtures.rest import BaseFixtureServiceRest
from core.web.services.core.constants.http_headers import HttpHeaders
from openai import OpenAI


class BaseServiceHarqisGPT(BaseFixtureServiceRest):

    def __init__(self, config, **kwargs):
        super(BaseServiceHarqisGPT, self).__init__(config, **kwargs)
        api_key = self.config.app_data["api_key"]
        self.request\
            .add_header(HttpHeaders.AUTHORIZATION, f'Bearer {api_key}')

        self.native_client = OpenAI(api_key=api_key)

