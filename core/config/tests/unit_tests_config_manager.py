import unittest
from unittest.mock import MagicMock

from core.config.app_config import AppConfigManager


class TestAppConfigManager(unittest.TestCase):
    def setUp(self):
        # Mock the ConfigLoaderService
        self.mock_service = MagicMock()
        self.manager = AppConfigManager(self.mock_service)

        # Updated: service.config should be a dict[str, dict]
        self.configurations = {
            'configuration_1': {'app_id': 'app1', 'id': 'config1', 'data': 'Config data for app1'},
            'configuration_2': {'app_id': 'app2', 'id': 'config2', 'data': 'Config data for app2'},
            'configuration_3': {'app_id': 'app1', 'id': 'config3', 'data': 'Config data for app3'},
        }

    def test_load_successful(self):
        """Loads configs for an existing app_id without error and filters correctly."""
        self.mock_service.config = self.configurations

        # Should not raise; should keep only sections with app_id == 'app1'
        self.manager.load('app1')

        self.assertEqual(len(self.manager._current_app_configs), 2)
        self.assertSetEqual(
            set(self.manager._current_app_configs.keys()),
            {'configuration_1', 'configuration_3'}
        )

    def test_load_nonexistent_app_id(self):
        """Loading a non-existent app_id raises KeyError."""
        self.mock_service.config = self.configurations
        with self.assertRaises(KeyError):
            self.manager.load('appX')

    def test_get_successful(self):
        """Retrieves a specific configuration section by key."""
        self.mock_service.config = self.configurations
        self.manager.load('app1')

        result = self.manager.get(dict, 'configuration_1')
        self.assertEqual(result['app_id'], 'app1')
        self.assertEqual(result['id'], 'config1')

    def test_get_nonexistent_id(self):
        """Retrieving a missing section key raises KeyError."""
        self.mock_service.config = self.configurations
        self.manager.load('app1')

        with self.assertRaises(KeyError):
            self.manager.get(dict, 'nonexistent_id')


if __name__ == '__main__':
    unittest.main()
