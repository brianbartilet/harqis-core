import inspect
import logging

from logging import Logger

logging.basicConfig(level=logging.INFO)


def log_current_function(logger: Logger = None) -> str:
    """
    Logs the name of the function that called this utility function.

    Args:
        logger (logging.Logger, optional): The logger to use for logging the function name.
            If None, the standard print function is used.

    Uses the inspect module to retrieve the current execution frame and its caller.
    Then extracts the function name from the caller frame and logs it.
    """
    current_frame = inspect.currentframe()
    caller_frame = inspect.getouterframes(current_frame)
    function_name = caller_frame[1].function
    message = f"The current function name is: {function_name}"

    if logger:
        logger.info(message)
    else:
        print(message)

    return function_name


