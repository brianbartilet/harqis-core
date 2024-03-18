import unittest
from http import HTTPStatus as HttpStatus

from apps.apps_config import APPS_CONFIG
from apps.apps_config import AppName

from web.services.core.config.webservice import AppConfigWSClient

from apps.gpt.services.completions import BaseServiceGPTCompletions
from apps.gpt.dto.payload import PayloadGPT


class TestGPTServices(unittest.TestCase):

    def test_gpt_service(self):
        given_config_gpt = AppConfigWSClient(**APPS_CONFIG[AppName.API_GPT.value])
        given_service = BaseServiceGPTCompletions(given_config_gpt)
        given_payload = PayloadGPT(model=given_config_gpt.app_data['model'], prompt="tell me a joke")
        given_request = given_service.get_request_completion(given_payload)

        when = given_service.send_request(given_request)

        then = given_service.verify.common
        then.assert_that(when.status_code, then.equal_to(HttpStatus.OK))


