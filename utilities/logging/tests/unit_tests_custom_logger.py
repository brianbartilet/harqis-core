import os
import unittest
import logging

from unittest.mock import patch, mock_open
from utilities.logging.custom_logger import create_logger, load_logging_configuration, find_logging_config, file_name


class TestLogger(unittest.TestCase):
    @patch('logging.getLogger')
    def test_custom_logger_default_name(self, mock_get_logger):
        """
        Test that the custom_logger function uses the name of the calling function as the logger name when no name is provided.
        """
        mock_get_logger.return_value.name = 'test_custom_logger_default_name'
        logger = create_logger()
        mock_get_logger.assert_called_with('test_custom_logger_default_name')
        self.assertEqual(logger.name, 'test_custom_logger_default_name')

    @patch('logging.getLogger')
    def test_custom_logger_custom_name(self, mock_get_logger):
        """
        Test that the custom_logger function uses the provided name as the logger name.
        """
        mock_get_logger.return_value.name = 'my_custom_logger'
        logger = create_logger('my_custom_logger')
        mock_get_logger.assert_called_with('my_custom_logger')
        self.assertEqual(logger.name, 'my_custom_logger')

    @patch('os.path.dirname')
    @patch('os.getcwd')
    @patch('os.listdir')
    def test_find_logging_config(self, mock_listdir, mock_get_cwd, mock_dirname):
        """
        Test that the find_logging_config function correctly finds the logging configuration file in the directory tree.
        """
        mock_get_cwd.return_value = '/path/to'
        mock_dirname.side_effect = lambda x: '/path' if x == '/path/to' else '/'
        mock_listdir.side_effect = [['not_logging.yaml'], [file_name]]

        config_path = find_logging_config()
        expected_path = os.path.join('/path', file_name)
        self.assertEqual(config_path, expected_path)

    @patch('builtins.open', new_callable=mock_open, read_data='dummy_yaml_content')
    @patch('yaml.load', return_value={'version': 1})
    @patch('logging.config.dictConfig')
    @patch('utilities.logging.custom_logger.find_logging_config', return_value='/path/to/' + file_name)
    def test_load_logging_configuration(self, mock_find_logging_config, mock_dict_config, mock_yaml_load, mock_open):
        """
        Test that the load_logging_configuration function correctly loads the logging configuration from the YAML file.
        """
        logger = load_logging_configuration()
        mock_find_logging_config.assert_called_once()
        mock_open.assert_called_with('/path/to/' + file_name)
        mock_yaml_load.assert_called_once()
        mock_dict_config.assert_called_once()
        self.assertIsInstance(logger, logging.Logger)
