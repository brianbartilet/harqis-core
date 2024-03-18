import unittest
import os
from enum import Enum
from web.services.core.json import JsonObject
from config.app_config import AppConfig


class MockedTypeObject(JsonObject):
    """
    A mock configuration object that represents a valid configuration.
    """
    name: str
    url: str
    author: str


class MockedTypeObjectInvalid(JsonObject):
    """
    A mock configuration object that represents an invalid configuration with missing attributes.
    """
    invalid_name: str
    invalid_url: str


class MockedAppNames(Enum):
    """
    Enumeration of mocked application names for testing purposes.
    """
    APPLICATION_CONFIG = 'APPLICATION_CONFIG'
    ANOTHER_APPLICATION_CONFIG = 'ANOTHER_APPLICATION_CONFIG'
    INVALID = 'INVALID'


class TestAppConfig(unittest.TestCase):
    """
    Unit tests for the AppConfig class.
    """

    def test_app_config_initialization(self):
        """
        Test that AppConfig initializes correctly with valid input.
        """
        given_base_path = os.path.join(os.getcwd())  # base_path defaults to /tests, file_name="apps_config.yaml"
        when_app_config = AppConfig(MockedAppNames.APPLICATION_CONFIG, MockedTypeObject, base_path=given_base_path)
        self.assertEqual(when_app_config.config.name, 'Cool Application')

    def test_app_config_key_error(self):
        """
        Test that AppConfig raises a KeyError when an invalid application name is provided.
        """
        given_base_path = os.path.join(os.getcwd())
        with self.assertRaises(KeyError):
            AppConfig(MockedAppNames.INVALID, MockedTypeObject, base_path=given_base_path)
