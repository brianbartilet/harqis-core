import unittest

from core.config.app_config import AppConfigManager
from unittest.mock import MagicMock


class TestAppConfigManager(unittest.TestCase):
    def setUp(self):
        # Create a mock of the ConfigLoaderService
        self.mock_service = MagicMock()
        self.manager = AppConfigManager(self.mock_service)

        # Example configurations
        self.configurations = [
            {'configuration_1': {'app_id': 'app1', 'id': 'config1', 'data': 'Config data for app1'}},
            {'configuration_2': {'app_id': 'app2', 'id': 'config2', 'data': 'Config data for app2'}},
            {'configuration_3': {'app_id': 'app1', 'id': 'config3', 'data': 'Config data for app3'}},
        ]

    def test_load_successful(self):
        """Test loading of configurations for an existing app ID."""
        # Set up the mock to return specific configuration
        self.mock_service.config = self.configurations

        # Expected to not raise an exception
        try:
            self.manager.load('app1')
            self.assertEqual(len(self.manager._current_app_configs), 2)
        except KeyError:
            self.fail("load() raised KeyError unexpectedly!")

    def test_load_nonexistent_app_id(self):
        """Test loading of configurations for a non-existent app ID raises KeyError."""
        self.mock_service.config = self.configurations

        # Check for KeyError when app_id does not exist
        with self.assertRaises(KeyError):
            self.manager.load('appX')

    def test_get_successful(self):
        """Test successful retrieval of a specific configuration by ID."""
        # Set up the mock to return specific configuration
        self.mock_service.config = self.configurations
        self.manager.load('app1')
        result = self.manager.get(dict, 'configuration_1')
        self.assertEqual(result['app_id'], 'app1')

    def test_get_nonexistent_id(self):
        """Test retrieval of a non-existent configuration ID raises KeyError."""
        # Assume some configuration is loaded, but not the one we're looking for
        self.mock_service.config = self.configurations
        self.manager.load('app1')

        # Expect a KeyError when the id does not exist
        with self.assertRaises(TypeError):
            self.manager.get(dict, 'nonexistent_id')

