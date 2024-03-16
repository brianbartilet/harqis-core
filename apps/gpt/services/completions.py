from apps.gpt.base import BaseServiceHarqisGPT
from apps.gpt.dto.payload import PayloadGPT

from web.services.core.constants.http_methods import HttpMethod


class BaseServiceGPTCompletions(BaseServiceHarqisGPT):
    def __init__(self, config):
        super(BaseServiceGPTCompletions, self).__init__(config)

        self.request\
            .add_uri_parameter('engines')\
            .add_uri_parameter('{}'.format(self.config.app_data['model']))\
            .add_uri_parameter('completions')

    def get_request_completion(self, payload: PayloadGPT):
        self.request\
            .set_method(HttpMethod.POST)\
            .add_json_body(payload)

        return self.request.build()

