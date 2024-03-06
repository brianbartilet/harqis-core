from hamcrest import assert_that, has_items, equal_to, only_contains, has_item, empty, \
    greater_than_or_equal_to, contains_string


class AssertionHelper():

    def __init__(self):
        self.log = None

    def assert_that(self, arg1, arg2, arg3='Checkpoint Failed.'):
        try:
            assert_that(arg1=arg1, arg2=arg2, arg3=arg3)
        except AssertionError as error:
            self.log.error(str(error).replace("\n", ""))
            raise error

    def assert_that_list_are_equal(self, expected_list, actual_list):
        self.assert_that(actual_list, equal_to(expected_list))

    def assert_that_list_is_not_empty(self, actual_list):
        self.assert_that(actual_list, not empty())

    def assert_that_item_is_not_empty(self, actual_item):
        self.assert_that(actual_item, not empty())

    def assert_that_list_is_empty(self, actual_list):
        self.assert_that(actual_list, empty())

    def assert_items_are_equal(self, expected_item, actual_item):
        self.assert_that(actual_item, equal_to(expected_item))

    def assert_items_are_not_equal(self, expected_item, actual_item):
        self.assert_that(actual_item, not equal_to(expected_item))

    def assert_greater_than_or_equal(self, expected_item, actual_item):
        self.assert_that(actual_item, greater_than_or_equal_to(expected_item))
        assert_that(actual_item, greater_than_or_equal_to(expected_item))

    def assert_string_contains_text(self, expected_text, actual_text):
        self.assert_that(actual_text, contains_string(expected_text))