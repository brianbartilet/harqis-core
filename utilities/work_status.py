from .custom_logger import custom_logger
from enum import Enum
import functools


log = custom_logger("Work Status")


class WorkStatus(Enum):
    WIP = 'Work In Progress'
    TEST = 'Testing In Progress'


def mark_status(status: WorkStatus):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            log.warning("{0}: {1}".format(status.value, func.__name__))
            return func(*args, **kwargs)
        return wrapper

    return decorator
