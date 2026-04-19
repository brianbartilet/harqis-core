import os
import tempfile
import unittest
import logging

from unittest.mock import patch, mock_open
from core.utilities.logging.custom_logger import create_logger, load_logging_configuration, find_logging_config, file_name


class TestLogger(unittest.TestCase):
    @patch('logging.getLogger')
    def test_custom_logger_default_name(self, mock_get_logger):
        mock_get_logger.return_value.name = 'test_custom_logger_default_name'
        logger = create_logger()
        mock_get_logger.assert_called_with('test_custom_logger_default_name')
        self.assertEqual(logger.name, 'test_custom_logger_default_name')

    @patch('logging.getLogger')
    def test_custom_logger_custom_name(self, mock_get_logger):
        mock_get_logger.return_value.name = 'my_custom_logger'
        logger = create_logger('my_custom_logger')
        mock_get_logger.assert_called_with('my_custom_logger')
        self.assertEqual(logger.name, 'my_custom_logger')

    def test_find_logging_config_in_cwd(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            config_path = os.path.join(tmpdir, file_name)
            with open(config_path, 'w') as f:
                f.write('version: 1\n')
            with patch('os.getcwd', return_value=tmpdir):
                result = find_logging_config()
            self.assertEqual(result, config_path)

    def test_find_logging_config_walks_up_to_parent(self):
        with tempfile.TemporaryDirectory() as parent_dir:
            config_path = os.path.join(parent_dir, file_name)
            with open(config_path, 'w') as f:
                f.write('version: 1\n')
            child_dir = os.path.join(parent_dir, 'subproject')
            os.makedirs(child_dir)
            with patch('os.getcwd', return_value=child_dir):
                result = find_logging_config()
            self.assertEqual(result, config_path)

    def test_find_logging_config_project_config_takes_priority_over_bundled(self):
        # When a project-level logging.yaml exists it should be returned, not the bundled one
        with tempfile.TemporaryDirectory() as tmpdir:
            config_path = os.path.join(tmpdir, file_name)
            with open(config_path, 'w') as f:
                f.write('version: 1\n')
            with patch('os.getcwd', return_value=tmpdir):
                result = find_logging_config()
            self.assertEqual(result, config_path)
            # Confirm the bundled core path was not returned
            import core.utilities.logging.custom_logger as mod
            core_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(mod.__file__))))
            bundled = os.path.join(core_dir, file_name)
            self.assertNotEqual(result, bundled)

    def test_find_logging_config_falls_back_to_bundled(self):
        # When no project-level logging.yaml is found, the bundled core one is returned
        with patch('os.getcwd', return_value='/'), \
             patch('os.listdir', return_value=[]):
            result = find_logging_config()
        self.assertIsNotNone(result)
        self.assertTrue(result.endswith(file_name))
        self.assertIn('core', result)

    def test_find_logging_config_returns_none_when_no_config_anywhere(self):
        with patch('os.getcwd', return_value='/'), \
             patch('os.listdir', return_value=[]), \
             patch('os.path.isfile', return_value=False):
            result = find_logging_config()
        self.assertIsNone(result)

    @patch('builtins.open', new_callable=mock_open, read_data='dummy_yaml_content')
    @patch('yaml.load', return_value={'version': 1})
    @patch('logging.config.dictConfig')
    @patch('core.utilities.logging.custom_logger.find_logging_config', return_value='/path/to/' + file_name)
    def test_load_logging_configuration(self, mock_find_logging_config, mock_dict_config, mock_yaml_load, mock):
        logger = load_logging_configuration()
        mock_find_logging_config.assert_called_once()
        mock.assert_called_with('/path/to/' + file_name)
        mock_yaml_load.assert_called_once()
        mock_dict_config.assert_called_once()
        self.assertIsInstance(logger, logging.Logger)

    @patch('core.utilities.logging.custom_logger.find_logging_config', return_value=None)
    def test_load_logging_configuration_raises_when_no_config(self, mock_find):
        with self.assertRaises(NotImplementedError):
            load_logging_configuration()
