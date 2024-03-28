import unittest
import os
import yaml

from urllib.parse import urlparse
from uuid import uuid4
from core.utilities.resources.download_file import ServiceDownloadFile
from http import HTTPStatus

from core.config.env_variables import Environment, ENV


class TestDownloadFile(unittest.TestCase):
    def setUp(self):
        self.get_url = "https://api.github.com/repos/brianbartilet/harqis-core/zipball/"
        self.get_url_file = \
            "https://raw.githubusercontent.com/OAI/OpenAPI-Specification/main/examples/v3.0/api-with-examples.yaml"

        self.file_name = f"harqis-core-{uuid4()}.zip"
        self.base_path = os.path.dirname(os.path.abspath(__file__))

    @unittest.skipIf(ENV != Environment.DEV.value, "Skipping tests for non-development environment.")
    def test_download_file(self):
        service = ServiceDownloadFile(url=self.get_url)
        service.download_file(file_name=self.file_name, path=self.base_path)

        file_path = os.path.join(self.base_path, self.file_name)
        self.assertTrue(os.path.exists(file_path))

    @unittest.skipIf(ENV != Environment.DEV.value, "Skipping tests for non-development environment.")
    def test_download_file_from_url_file(self):
        service = ServiceDownloadFile(url=self.get_url_file)

        url_path = urlparse(self.get_url_file).path
        self.file_name = os.path.basename(url_path)

        response = service.download_file(file_name=self.file_name, path=self.base_path)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        file_path = os.path.join(self.base_path, self.file_name)
        self.assertTrue(os.path.exists(file_path))

    def test_download_file_static(self):
        service = ServiceDownloadFile(url=self.get_url)
        response = service.download_file(file_name=self.file_name)
        self.assertEqual(response.status_code, HTTPStatus.OK)


