from apps.sprout.core.celery import SPROUT


@SPROUT.task()
def test_run_add(a: int, b: int):
    """Test function to add two numbers and return the result."""
    return a + b


