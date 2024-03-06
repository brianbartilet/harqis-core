import unittest
from runners.tests_runner import *

class TestsUnitTestRunner(unittest.TestCase):
    def test_run_unit_tests_mp(self):
        runner = UnitTestLauncher(multiprocessing=False)
        runner.run_tests()

