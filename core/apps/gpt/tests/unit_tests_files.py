import unittest

from core.apps.gpt.services.files import ServiceFiles
from core.apps.apps_config import AppConfigLoader, AppNames
from http import HTTPStatus


class TestServiceAssistant(unittest.TestCase):

    def setUp(self):
        """
        Set up the test environment by initializing the GPT service and payload.
        """
        self.given_config = AppConfigLoader(AppNames.API_GPT).config
        self.given_service = ServiceFiles(self.given_config)
        self.then = self

    def test_simple_flow_file_upload_download(self):
        when_upload_file = self.given_service.upload_file(file_name='sample.txt')
        self.then.assertGreater(when_upload_file.bytes, 0)

        when_list_files = self.given_service.get_files()
        self.then.assertIn(when_upload_file, when_list_files)
