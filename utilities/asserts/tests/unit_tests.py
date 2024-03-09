import unittest
from unittest.mock import MagicMock
from utilities.asserts.helper import LoggedAssertHelper, raise_any_exception, is_between
from hamcrest import *

class TestLoggedAssertHelper(unittest.TestCase):

    def setUp(self):
        self.report_generator = MagicMock()
        self.assert_helper = LoggedAssertHelper(report_generator=self.report_generator)

    def test_assert_items_are_not_equal_success(self):
        expected = [1, 2, 3]
        actual = [4, 5, 6]
        self.assert_helper.assert_items_are_not_equal(expected, actual)
        self.report_generator.append_row.assert_called_with(['SUCCESS', actual, 'is not equal to', expected])

    def test_assert_items_are_not_equal_failure(self):
        expected = [1, 2, 3]
        actual = [1, 2, 3]
        with self.assertRaises(AssertionError):
            self.assert_helper.assert_items_are_not_equal(expected, actual)
        self.report_generator.append_row.assert_called_with(['FAILURE', actual, 'is not equal to', expected])

    def test_assert_numbers_are_equal_within_tolerance_success(self):
        expected = 100
        actual = 101
        tolerance = 1
        self.assert_helper.assert_numbers_are_equal(expected, actual, tolerance)
        self.report_generator.append_row.assert_called_with(['SUCCESS', actual, 'is equal to', expected, 'tolerance: 1%'])

    def test_assert_numbers_are_equal_within_tolerance_failure(self):
        expected = 100
        actual = 103
        tolerance = 1
        with self.assertRaises(AssertionError):
            self.assert_helper.assert_numbers_are_equal(expected, actual, tolerance)
        self.report_generator.append_row.assert_called_with(['FAILURE', actual, 'is equal to', expected, 'tolerance: 1%'])

    def test_assert_each_item_in_list_between_success(self):
        actual_list = [2, 3, 4]
        lower_bound = 1
        upper_bound = 5
        self.assert_helper.assert_each_item_in_list_between(actual_list, lower_bound, upper_bound)
        for actual in actual_list:
            self.report_generator.append_row.assert_any_call(['SUCCESS', actual, 'is between', f'{lower_bound} and {upper_bound}'])

    def test_assert_each_item_in_list_between_failure(self):
        actual_list = [2, 3, 6]
        lower_bound = 1
        upper_bound = 5
        with self.assertRaises(AssertionError):
            self.assert_helper.assert_each_item_in_list_between(actual_list, lower_bound, upper_bound)
        self.report_generator.append_row.assert_any_call(['FAILURE', 6, 'is between', f'{lower_bound} and {upper_bound}'])

    def test_assert_each_item_in_list_greater_than_success(self):
        expected = 0
        actual_list = [1, 2, 3]
        self.assert_helper.assert_each_item_in_list_greater_than(expected, actual_list)
        for actual in actual_list:
            self.report_generator.append_row.assert_any_call(['SUCCESS', actual, 'is greater than', expected])

    def test_assert_each_item_in_list_greater_than_failure(self):
        expected = 2
        actual_list = [1, 2, 3]
        with self.assertRaises(AssertionError):
            self.assert_helper.assert_each_item_in_list_greater_than(expected, actual_list)
        self.report_generator.append_row.assert_any_call(['FAILURE', 1, 'is greater than', expected])

    def test_raise_any_exception(self):
        exception_list = ["Error 1", "Error 2"]
        with self.assertRaises(AssertionError) as context:
            raise_any_exception(exception_list)
        self.assertIn("Error(s) encountered: Error 1\nError 2", str(context.exception))

    def test_is_between(self):
        matcher = is_between(1, 5)
        assert_that(3, matcher)
        assert_that(1, matcher)
        assert_that(5, matcher)
        with self.assertRaises(AssertionError):
            assert_that(0, matcher)
        with self.assertRaises(AssertionError):
            assert_that(6, matcher)

