from enum import Enum


class EnvSettings(Enum):
    """
    Enum class for environment settings.

    Attributes:
        DEV (str): Represents the development environment.
        PROD (str): Represents the production environment.
    """

    DEV = 'DEV'
    PROD = 'PROD'
