from functools import wraps
from core.utilities.logging.custom_logger import create_logger

log = create_logger("Loading Gherkin decorators")


def given(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        log.info(f"Given: {func.__name__}")
        return func(*args, **kwargs)
    wrapper.__test_phase__ = 'given'
    return wrapper


def when(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        log.info(f"When: {func.__name__}")
        return func(*args, **kwargs)
    wrapper.__test_phase__ = 'when'
    return wrapper


def then(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        log.info(f"Then: {func.__name__}")
        return func(*args, **kwargs)
    wrapper.__test_phase__ = 'then'
    return wrapper
