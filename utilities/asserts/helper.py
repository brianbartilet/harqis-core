import hamcrest
from hamcrest import *

from reports.report_generator import ReportGenerator

def raise_any_exception(exception_list: list) -> None:
    """
    Raises an AssertionError with a concatenated message of all exceptions in the list.

    Args:
        exception_list (list): A list of exception messages.

    Raises:
        AssertionError: An error with a concatenated message of all exceptions.
    """
    if len(exception_list) > 0:
        all_exceptions = "\n".join([str(exc) for exc in exception_list])
        full_message = f"Error(s) encountered: {all_exceptions}"
        raise AssertionError(full_message)

def is_between(lower_bound, upper_bound):
    """
    Returns a matcher that checks if a value is between two bounds.

    Args:
        lower_bound: The lower bound of the range.
        upper_bound: The upper bound of the range.

    Returns:
        A Hamcrest matcher that checks if a value is between the specified bounds.
    """
    return all_of(greater_than_or_equal_to(lower_bound), less_than_or_equal_to(upper_bound))

class LoggedAssertHelper:
    """
    A helper class for performing assertions and logging the results.

    """

    @property
    def common(self):
        """
        Provides access to common Hamcrest matchers.

        Returns:
            The hamcrest module with common matchers.
        """
        return hamcrest

    def __init__(self, report_generator: ReportGenerator = None):
        """
        Initializes the LoggedAssertHelper with an optional report generator.

        Args:
            report_generator (ReportGenerator, optional): An instance of ReportGenerator for logging assertion results. Defaults to None.
        """
        self.__report_generator = report_generator

    def assert_items_are_not_equal(self, expected: list, actual: list):
        """
        Asserts that two lists are not equal and logs the result.

        Args:
            expected (list): The expected list.
            actual (list): The actual list to compare.

        Raises:
            AssertionError: If the actual list is equal to the expected list.
        """
        try:
            assert_that(actual, is_not(expected))
            self.__write_report_entry__('SUCCESS', actual, 'is not equal to', expected)
        except AssertionError:
            self.__write_report_entry__('FAILURE', actual, 'is not equal to', expected)
            raise

    def assert_items_in_list_are_equal_unordered(self, expected: list, actual: list):
        """
        Asserts that two lists contain the same items in any order and logs the result.

        Args:
            expected (list): The expected list.
            actual (list): The actual list to compare.

        Raises:
            AssertionError: If the actual list does not contain the same items as the expected list.
        """
        self._check_list_lengths(expected, actual)
        for item in expected:
            self.assert_item_in_list(actual, item)

    def assert_item_not_in_list(self, expected: list, actual_item):
        """
        Asserts that an item is not in a list and logs the result.

        Args:
            expected (list): The list to check.
            actual_item: The item that should not be in the list.

        Raises:
            AssertionError: If the item is in the list.
        """
        try:
            assert_that(actual_item, not_(is_in(expected)))
            self.__write_report_entry__('SUCCESS', actual_item, 'is not in list', expected)
        except AssertionError:
            self.__write_report_entry__('FAILURE', actual_item, 'is not in list', expected)
            raise

    def assert_item_in_list(self, expected: list, actual_item):
        """
        Asserts that an item is in a list and logs the result.

        Args:
            expected (list): The list to check.
            actual_item: The item that should be in the list.

        Raises:
            AssertionError: If the item is not in the list.
        """
        try:
            assert_that(actual_item, is_in(expected))
            self.__write_report_entry__('SUCCESS', actual_item, 'is in list', expected)
        except AssertionError:
            self.__write_report_entry__('FAILURE', actual_item, 'is in list', expected)
            raise

    def assert_each_item_in_list_are_equal(self, expected: list, actual: list, tolerance=None):
        """
        Asserts that each corresponding item in two lists are equal and logs the result.

        Args:
            expected (list): The expected list.
            actual (list): The actual list to compare.
            tolerance (float, optional): The tolerance for numerical comparisons. Defaults to None.

        Raises:
            AssertionError: If any corresponding items in the lists are not equal.
        """
        self._check_list_lengths(expected, actual)
        for exp, act in zip(expected, actual):
            self.assert_items_are_equal(exp, act, tolerance)

    def assert_rows_are_equal(self, expected: list, actual: list, tolerance: float = None):
        """
        Asserts that each row (list) in two lists of rows are equal and logs the result.

        Args:
            expected (list): The expected list of rows.
            actual (list): The actual list of rows to compare.
            tolerance (float, optional): The tolerance for numerical comparisons within rows. Defaults to None.

        Raises:
            AssertionError: If any row in the lists is not equal.
        """
        self._check_list_lengths(expected, actual)
        for exp, act in zip(expected, actual):
            self.assert_each_item_in_list_are_equal(exp, act, tolerance)

    def assert_items_are_equal(self, expected, actual, tolerance=None):
        """
        Asserts that two items are equal and logs the result.

        Args:
            expected: The expected item.
            actual: The actual item to compare.
            tolerance (float, optional): The tolerance for numerical comparisons. Defaults to None.

        Raises:
            AssertionError: If the items are not equal.
        """
        if isinstance(actual, (int, float)) and tolerance is not None:
            self.assert_numbers_are_equal(expected, actual, tolerance)
        else:
            try:
                assert_that(actual, equal_to(expected))
                self.__write_report_entry__('SUCCESS', actual, 'is equal to', expected)
            except AssertionError:
                self.__write_report_entry__('FAILURE', actual, 'is equal to', expected)
                raise

    def assert_numbers_are_equal(self, expected, actual, tolerance: float):
        """
        Asserts that two numbers are equal within a tolerance and logs the result.

        Args:
            expected (float): The expected number.
            actual (float): The actual number to compare.
            tolerance (float): The tolerance for the comparison.

        Raises:
            AssertionError: If the numbers are not equal within the tolerance.
        """
        lower_bound = expected * (1 - tolerance / 100)
        upper_bound = expected * (1 + tolerance / 100)
        try:
            assert_that(actual, is_between(lower_bound, upper_bound))
            self.__write_report_entry__('SUCCESS', actual, 'is equal to', expected, tolerance)
        except AssertionError:
            self.__write_report_entry__('FAILURE', actual, 'is equal to', expected, tolerance)
            raise

    def assert_each_item_in_list_between(self, actual_list: list, lower_bound, upper_bound):
        """
        Asserts that each item in a list is between two bounds and logs the result.

        Args:
            actual_list (list): The list of items to check.
            lower_bound: The lower bound of the range.
            upper_bound: The upper bound of the range.

        Raises:
            AssertionError: If any item in the list is not between the bounds.
        """
        for actual in actual_list:
            try:
                assert_that(actual, is_between(lower_bound, upper_bound))
                self.__write_report_entry__('SUCCESS', actual, 'is between', f'{lower_bound} and {upper_bound}')
            except AssertionError:
                self.__write_report_entry__('FAILURE', actual, 'is between', f'{lower_bound} and {upper_bound}')
                raise

    def assert_each_item_in_list_greater_than(self, expected, actual_list: list):
        """
        Asserts that each item in a list is greater than a specified value and logs the result.

        Args:
            expected: The value that each item in the list should be greater than.
            actual_list (list): The list of items to check.

        Raises:
            AssertionError: If any item in the list is not greater than the specified value.
        """
        for actual in actual_list:
            try:
                assert_that(actual, greater_than(expected))
                self.__write_report_entry__('SUCCESS', actual, 'is greater than', expected)
            except AssertionError:
                self.__write_report_entry__('FAILURE', actual, 'is greater than', expected)
                raise

    def _check_list_lengths(self, expected, actual):
        """
        Checks if the lengths of two lists are equal and logs the result.

        Args:
            expected (list): The expected list.
            actual (list): The actual list to compare.

        Raises:
            AssertionError: If the lengths of the lists are not equal.
        """
        try:
            assert_that(len(actual), equal_to(len(expected)))
        except AssertionError:
            diff = list(set(expected) - set(actual)) + list(set(actual) - set(expected))
            error_message = f"Lengths not equal: expected {len(expected)}, actual {len(actual)}\nDifferences: {diff}"
            self.__write_any_entry__(error_message)
            raise AssertionError(error_message)

    def __write_report_entry__(self, status, actual, message, expected, tolerance=None):
        """
        Writes a report entry for an assertion.

        Args:
            status (str): The status of the assertion (e.g., 'SUCCESS' or 'FAILURE').
            actual: The actual value involved in the assertion.
            message (str): The message describing the assertion.
            expected: The expected value involved in the assertion.
            tolerance (float, optional): The tolerance used in the assertion, if applicable.

        """
        entry = [status, actual, message, expected]
        if tolerance is not None:
            entry.append(f'tolerance: {tolerance}%')
        self.__write_any_entry__(entry)

    def __write_any_entry__(self, entry):
        """
        Writes any entry to the report generator.

        Args:
            entry: The entry to be written to the report.
        """
        if self.__report_generator is not None:
            self.__report_generator.append_row(entry)
