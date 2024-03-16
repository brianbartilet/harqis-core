from enum import Enum


class AppName(Enum):
    """
    Enum class for environment settings.

    Attributes:
        DEV (str): Represents the development environment.
        PROD (str): Represents the production environment.
    """

    API_GPT = 'HARQIS_GPT'
