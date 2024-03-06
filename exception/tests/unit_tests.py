import unittest
from exception.error_wrapper import *
import pytest

class TestsExceptionHandler(unittest.TestCase):

    @handle_exception(NotImplementedError, "Not Implemented Code", ignore_exception=True)
    def test_not_implemented(self):
        with pytest.raises(NotImplementedError):
            raise NotImplementedError

    @handle_exception(NotImplementedError, "Not Implemented Code", ignore_exception=False)
    def test_not_implemented_false(self):
        with pytest.raises(NotImplementedError):
            raise NotImplementedError
