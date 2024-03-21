from enum import Enum


class Environment(Enum):
    """
    Enum class for environment settings.

    Attributes:
        DEV (str): Represents the development environment.
        PROD (str): Represents the production environment.
    """

    DEV = 'DEV'
    PROD = 'PROD'
    TEST = 'TEST'
