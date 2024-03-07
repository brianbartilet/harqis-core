from enum import Enum

class AssertionMessages(Enum):
    SUCCESS_MESSAGE = "PASSED"
    FAILURE_MESSAGE = "FAILED"
    EQUAL_MESSAGE = "should be equal to"
    UNEQUAL_MESSAGE = "should not be equal to"
    BETWEEN_MESSAGE = "should be between"
    GREATER_MESSAGE = "should be greater than"
    CONTAINS_MESSAGE = "should be in"
    NOT_CONTAINS_MESSAGE = "should not be in"

class AssertionErrorMessages(Enum):
    ERROR_LENGTH_NOT_EQUAL = "Error: lengths are not equal"
    ERROR_VALUES_NOT_EQUAL = "Error: values being compared are not equal"