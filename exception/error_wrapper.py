"""
Provide friendly error messages from error classes and their traceback

"""

import functools
import inspect
import sys
import traceback

from utilities.logging.custom_logger import custom_logger


class BaseExceptionWrapperDto:
    def __init__(self, **kwargs):
        self.title = kwargs.get('title', '')
        self.error_class = kwargs.get('class_error', '')
        self.text = kwargs.get('text', '')
        self.message = kwargs.get('message', '')
        self.file = kwargs.get('file', '')
        self.line = kwargs.get('line', '')


class BaseExceptionWrapper(Exception):
    """Common Base class for custom Exception handler"""
    log = custom_logger()
    output = """
    [{title}]:
        Class: {class_error}
        Page: {page}
        File: {file}
        Line: {line}
        Element Key: {element_key}
        Locator Type: {locator_type}
        Locator Value: {locator_value}
        Message: {text} {message}      
    """

    def __init__(self, message_dto):
        super().__init__()
        message_dto.title = "CAPTURED EXCEPTION"
        if not message_dto.text == "":
            message_dto.text = "'" + message_dto.text + "'"

        self.log.info(self.output.format(**message_dto.__dict__))


class IgnoreException(BaseExceptionWrapper):
    """ Ignore all encountered exception """

    def __init__(self, message_dto: BaseExceptionWrapperDto):
        message_dto.title = "IGNORED EXCEPTION"
        if not message_dto.text == "":
            message_dto.text = "'" + message_dto.text + "'"
        self.log.warning("[" + message_dto.title + "] Class: " + message_dto.error_class +
                         " File: " + message_dto.file + " Line: " + str(message_dto.line))


def handle_exception(exception,
                     description,
                     ignore_exception=False,
                     return_condition=False):
    """
    Decorator to wrap a method with custom exception handling.  Can support multiple definitions
    and drives all exception handling to the selenium driver class.  Process 'locator' signature
    from arguments to work with get_key_dic() to show locator dictionary definition
    :param exception: pass exception class from builtins or from other libraries
    :param description: description text for exception captured
    :param ignore_exception: enable warnings on ignored exception
    :param return_condition: configure return boolean value when exception is encountered
            this is used for presence check functions to return desired condition
    """
    def decorator(func):
        signature = inspect.signature(func)

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)

            except exception:
                """
                    check the exception info to pass additional information to the exception handler
                """
                exc_info = sys.exc_info()
                stack = traceback.extract_stack()
                tb = traceback.extract_tb(exc_info[2])
                full_tb = stack[:-1] + tb

                """
                handle unwrapped calls and show traceback from selenium driver native calls
                """

                target_tb = full_tb[-1]
                target_tb = full_tb[-2] if "site-packages" in target_tb.filename\
                    or "exception_handler" in target_tb.filename else full_tb[-1]

                line = str(target_tb.lineno)
                file = target_tb.filename

                """
                check the arguments in wrapped functions for specific signatures to be passed to the exception message
                e.g. 'locator', 'locator_type', 'text'
                we would need to have a standard for the parameter names in the driver class so it can properly process
                the parameter values to the display, this can still be updated if desired
                """
                arg_element_key = arg_locator_type = arg_locator = arg_text = ''

                dto = BaseExceptionWrapperDto(
                    class_error=exception.__name__,
                    page=args[0].__class__.__name__,
                    element_key=arg_element_key,
                    locator_type=arg_locator_type,
                    locator_value=arg_locator,
                    text=arg_text,
                    message=description,
                    file=file,
                    line=line
                )

                if ignore_exception:
                    IgnoreException(dto)
                else:
                    raise BaseExceptionWrapper(dto)

                return return_condition

        return wrapper

    return decorator






