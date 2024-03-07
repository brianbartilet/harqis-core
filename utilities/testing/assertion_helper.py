from hamcrest import *
import hamcrest
from utilities.report_generator import ReportGenerator

error_length_not_equal = "Error: lengths are not equal"
error_values_not_equal = "Error: values being compared are not equal"

class LoggedAssertHelper():
    SUCCESS_MESSAGE = "Passed"
    FAILURE_MESSAGE = "Failed"
    EQUAL_MESSAGE = "should be equal to"
    UNEQUAL_MESSAGE = "should not be equal to"
    BETWEEN_MESSAGE = "should be between"
    GREATER_MESSAGE = "should be greater than"
    CONTAINS_MESAGE = "should be in"
    NOT_CONTAINS_MESSAGE = "should not be in"

    @property
    def common(self):
        return hamcrest

    def __init__(self, report_generator: ReportGenerator = None):
        # we need context here to get access to the report_generator
        self.__report_generator = report_generator

    def assert_items_are_not_equal(self, expected, actual):
        try:
            assert_that(actual, is_not(expected))
            self.__write_success_not_equal__(expected, actual)
        except:
            self.__write_failure_not_equal__(expected, actual)
            raise

    def assert_items_in_list_are_equal_unordered(self, expected: list, actual: list):
        # check lengths first
        self.__write_any_entry__("Checking list are equal in any order:")

        self._check_list_lengths(expected, actual)

        self.assert_items_in_unordered_list_with_length_varying(expected, actual)

    def assert_item_not_in_list(self, expected : list, actual_item):

        self.__write_any_entry__("Checking if item in list:")

        try:
            assert_that(actual_item, not_(is_in(expected)))
            self.__write_success_not_contains__(expected, actual_item)
        except:
            self.__write_failure_not_contains__(expected, actual_item)
            raise

    def assert_item_in_list(self, expected : list, actual_item):

        self.__write_any_entry__("Checking if item in list:")

        try:
            assert_that(actual_item, not_(is_in(expected)))
            self.__write_success_contains__(expected, actual_item)
        except:
            self.__write_failure_contains__(expected, actual_item)
            raise

    def assert_each_item_in_list_are_equal(self, expected: list, actual: list, tolerance = None):
        """
            The items here are tested
        :param tolerance:
        :param expected:
        :param actual:
        :return:
        """
        # do a prelimenary assert
        self._check_list_lengths(expected, actual)

        self.__write_any_entry__("Checking list are equal in order:")
        failure_list = []
        for exp, act in zip(expected, actual):
            try:
                self.assert_items_are_equal(exp, act, tolerance)
            except AssertionError as e:
                failure_list.append(e)

        self.__raise_any_exception__(failure_list)

    def assert_rows_are_equal(self, expected: list, actual:list, tolerance : float = None):

        error_message = ""

        self._check_list_lengths(expected, actual)

        # if there is an error, do the item per item assert
        failure_list = []
        for exp, act in zip(expected, actual):
            # now check the next
            try:
                self.assert_each_item_in_list_are_equal(exp, act, tolerance)
            except AssertionError as e:
                failure_list.append(e)

        self.__raise_any_exception__(failure_list)

    def assert_items_are_equal(self, expected, actual, tolerance = None):

        # first get the type of the item
        if (isinstance(actual, int) or isinstance(actual, float))\
            and tolerance is not None:
            self.assert_numbers_are_equal(expected, actual, tolerance)
        else:
            try:
                assert_that(actual, equal_to(expected))
                self.__write_success_equal__(expected, actual)
            except:
                self.__write_failure_equal__(expected, actual)
                raise

    def assert_numbers_are_equal(self, expected, actual, tolerance : float):
        """

        :param expected:
        :param actual:
        :param tolerance: this should be in percentage. e.g., pass 1 if it is for 1%
        :return:
        """
        if isinstance(tolerance, int) or isinstance(tolerance, float):

            lower_bound = expected*(1 - (tolerance/100))
            upper_bound = expected*(1 + (tolerance/100))

            # need to change - this is for managing negative signs
            actual_lower_bound = (upper_bound, lower_bound)[lower_bound < upper_bound]
            actual_upper_bound = (lower_bound, upper_bound)[lower_bound < upper_bound]
            try:

                assert_that(actual,  self.__is_between__(actual_lower_bound, actual_upper_bound))
                self.__write_success_equal__(expected, actual, tolerance)
            except AssertionError as e:
                self.__write_failure_equal__(expected, actual, tolerance)
                raise e
        else:
            raise TypeError("tolerance value not allowed. Please use integer or float types")

    def assert_each_item_in_list_between(self, actual_list: list, lower_bound, upper_bound):
        failure_list = []
        for actual in actual_list:
            try:

                assert_that(actual, self.__is_between__(lower_bound, upper_bound))
                self.__write_success_between__(actual, lower_bound, upper_bound)
            except AssertionError as e:
                self.__write_failure_equal__(actual, lower_bound, upper_bound)
                failure_list.append(e)

        self.__raise_any_exception__(failure_list)

    def assert_each_item_in_list_greater_than(self, expected, actual_list: list):
        failure_list = []
        for actual in actual_list:
            try:

                assert_that(actual, all_of(greater_than(expected)))
                self.__write_success_greater__(expected, actual)
            except AssertionError as e:
                self.__write_failure_greater__(expected, actual)
                failure_list.append(e)

        self.__raise_any_exception__(failure_list)

    def __is_between__(self, lower_bound, upper_bound):
        """
        helper method for
        :param lower_bound:
        :param upper_bound:
        :return:
        """
        return all_of(greater_than_or_equal_to(lower_bound), less_than_or_equal_to(upper_bound))

    def generate_list_from_context_table(self, context_table):
        '''

        :param context_table: behave context table as input
        :return: returns context table items as list of items
        '''
        exp_list = []
        exp_row_item = []
        for row in context_table.rows:
            for cell in row:
                exp_row_item.append(cell)
            exp_list.append(exp_row_item)
            exp_row_item = []

        return exp_list

    def generate_list_from_db_select_query(self, select_query_items):
        '''

        :param select_query_items:
        :return: select query items as list of items
        '''
        act_list = []
        for item in select_query_items:
            act_list.append(list(item))

        return act_list

    def assert_items_in_unordered_list_with_length_varying(self, expected_items : list, actual_items : list):
       '''
       :param expected_items:
       :param actual_items:
       :return:
       '''
       for expected in expected_items:
           try:
               assert_that(actual_items, has_item(expected))
           except:
               self.__write_any_entry__("Item not found: {}".format(expected))
               raise

       self.__write_any_entry__("All expected in actual list")
       self.__write_any_entry__("Actual list: {}".format(actual_items))
       self.__write_any_entry__("Expected list: {}".format(expected_items))

    def get_report_generator(self) -> ReportGenerator:
        return self.__report_generator

    def _check_list_lengths(self, expected, actual):
        self.__write_any_entry__("Checking lengths:")

        try:
            assert_that(len(actual), equal_to(len(expected)))
            self.__write_success_equal__(len(expected), len(actual))
        except AssertionError as e:
            diff = (list(set(expected) - set(actual)), list(set(actual) - set(expected)))[len(actual) > len(expected)]
            error_message = "{} not equal to expected {}\n".format(str(len(actual)), str(len(expected)))
            error_message += "differences: \n {}".format('\n'.join(str(item) for item in diff))

            self.__write_any_entry__(error_message)

            raise AssertionError(error_message)

    def __raise_any_exception__(self, exception_list : list) -> None:
        if len(exception_list) > 0:
            all_exceptions = "\n".join([str(exc) for exc in exception_list])
            full_message = "Error(s) encountered: {}".format(all_exceptions)
            raise AssertionError(full_message)


    def __write_failure_not_equal__(self, expected, actual, tolerance = None):
        self.__write_report_entry__(LoggedAssertHelper.FAILURE_MESSAGE, expected, actual, LoggedAssertHelper.UNEQUAL_MESSAGE, tolerance)

    def __write_success_not_equal__(self, expected, actual, tolerance = None):
        self.__write_report_entry__(LoggedAssertHelper.SUCCESS_MESSAGE, expected, actual, LoggedAssertHelper.UNEQUAL_MESSAGE, tolerance)

    def __write_failure_equal__(self, expected, actual, tolerance = None):
        self.__write_report_entry__(LoggedAssertHelper.FAILURE_MESSAGE, expected, actual, LoggedAssertHelper.EQUAL_MESSAGE, tolerance)

    def __write_success_between__(self, actual, lower_bound, upper_bound):
        full_message = "{} {} and {}".format(LoggedAssertHelper.BETWEEN_MESSAGE, lower_bound, upper_bound)
        self.__write_any_entry__([LoggedAssertHelper.SUCCESS_MESSAGE, actual, full_message])

    def __write_failure_between__(self, actual, lower_bound, upper_bound):
        full_message = "{} {} and {}".format(LoggedAssertHelper.BETWEEN_MESSAGE, lower_bound, upper_bound)
        self.__write_any_entry__([LoggedAssertHelper.FAILURE_MESSAGE, actual, full_message])

    def __write_success_equal__(self, expected, actual, tolerance = None):
        self.__write_report_entry__(LoggedAssertHelper.SUCCESS_MESSAGE, expected, actual, LoggedAssertHelper.EQUAL_MESSAGE, tolerance)

    def __write_success_greater__(self, expected, actual, tolerance = None):
        self.__write_report_entry__(LoggedAssertHelper.SUCCESS_MESSAGE, expected, actual, LoggedAssertHelper.GREATER_MESSAGE, tolerance)

    def __write_failure_greater__(self, expected, actual, tolerance = None):
        self.__write_report_entry__(LoggedAssertHelper.FAILURE_MESSAGE, expected, actual, LoggedAssertHelper.GREATER_MESSAGE, tolerance)

    def __write_success_contains__(self, expected, actual, tolerance = None):
        self.__write_report_entry__(LoggedAssertHelper.SUCCESS_MESSAGE, expected, actual, LoggedAssertHelper.CONTAINS_MESAGE, tolerance)

    def __write_success_not_contains__(self, expected, actual, tolerance = None):
        self.__write_report_entry__(LoggedAssertHelper.SUCCESS_MESSAGE, expected, actual, LoggedAssertHelper.NOT_CONTAINS_MESSAGE, tolerance)

    def __write_failure_contains__(self, expected, actual, tolerance = None):
        self.__write_report_entry__(LoggedAssertHelper.FAILURE_MESSAGE, expected, actual, LoggedAssertHelper.CONTAINS_MESAGE, tolerance)

    def __write_failure_not_contains__(self, expected, actual, tolerance = None):
        self.__write_report_entry__(LoggedAssertHelper.FAILURE_MESSAGE, expected, actual, LoggedAssertHelper.NOT_CONTAINS_MESSAGE, tolerance)


    def __write_report_entry__(self, result, expected, actual, equality_message, tolerance = None):
        if tolerance is not None:
            tolerance_string = "tolerance: {}%".format(tolerance)
            self.__write_any_entry__([result, actual, equality_message, expected, tolerance_string])
        else:
            self.__write_any_entry__([result, actual, equality_message, expected])

    def __write_any_entry__(self, entry):
        if self.__report_generator is not None:
            self.__report_generator.append_row(entry)
