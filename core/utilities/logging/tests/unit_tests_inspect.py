import unittest
from unittest.mock import MagicMock
from core.utilities.logging.inspect import log_current_function  # Replace 'your_module' with the actual module name


class TestLogCurrentFunction(unittest.TestCase):
    def test_log_current_function_with_logger(self):
        # Set up a mock logger
        mock_logger = MagicMock()

        # Call the function with the mock logger
        log_current_function(mock_logger)

        # Assert that the logger's info method was called with a message containing the function name
        mock_logger.info.assert_called_with("The current function name is: test_log_current_function_with_logger")



