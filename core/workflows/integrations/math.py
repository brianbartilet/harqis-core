from core.apps.sprout.core.celery import SPROUT


@SPROUT.task()
def add(a: int, b: int):
    """Test function to add two numbers and return the result."""
    return a + b


