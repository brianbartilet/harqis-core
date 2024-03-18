from enum import Enum

from config.environment_variables import ENV_ROOT_DIRECTORY
from config.loader import ConfigLoader


class AppName(Enum):
    """
    Enum class for environment settings.

    Attributes:
        DEV (str): Represents the development environment.
        PROD (str): Represents the production environment.
    """

    API_GPT = 'HARQIS_GPT'


# Load the application configuration from the specified file and base directory
APPS_CONFIG = ConfigLoader(base_path=ENV_ROOT_DIRECTORY).config