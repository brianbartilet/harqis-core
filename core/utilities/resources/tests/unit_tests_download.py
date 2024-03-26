import unittest
import os

from uuid import uuid4
from core.utilities.resources.download_file import ServiceDownloadFile
from http import HTTPStatus

from core.config.env_variables import Environment, ENV


class TestDownloadFile(unittest.TestCase):
    def setUp(self):
        self.get_url = "https://api.github.com/repos/brianbartilet/harqis-core/zipball/"
        self.file_name = f"harqis-core-{uuid4()}.zip"
        self.base_path = os.path.dirname(os.path.abspath(__file__))

    @unittest.skipIf(ENV != Environment.DEV.value, "Skipping tests for non-development environment.")
    def test_download_file(self):
        service = ServiceDownloadFile(url=self.get_url)
        service.download_file(file_name=self.file_name)

        file_path = os.path.join(self.base_path, self.file_name)
        self.assertTrue(os.path.exists(file_path))

    def test_download_file_statis(self):
        service = ServiceDownloadFile(url=self.get_url)
        response = service.download_file(file_name=self.file_name)
        self.assertEqual(response.status_code, HTTPStatus.OK)
