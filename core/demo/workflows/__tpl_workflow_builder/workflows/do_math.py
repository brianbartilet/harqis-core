from core.apps.sprout.app.celery import SPROUT
from random import randint


@SPROUT.task()
def add_random_numbers():
    """Test function to add two numbers and return the result."""
    return randint(1, 100) + randint(1, 100)


