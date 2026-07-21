from enum import Enum
from core.web.services.core.config.webservice import AppConfigWSClient
from core.config.app_config import AppConfig
from typing import TypeVar

TConfig = TypeVar("TConfig")


class AppNames(Enum):
    """
    Enum class for environment settings.

    Attributes:
        TASKS_CLIENT (str): Celery tasks client.
        ELASTIC_LOGGING (str): Elastic integration.
    """
    TASKS_CLIENT = 'CELERY_TASKS'
    ELASTIC_LOGGING = 'ELASTIC_LOGGING'

class AppConfigLoader(AppConfig):
    """
    A class that maps web service client names to their corresponding client classes.

    Attributes:
        map (dict): A dictionary mapping web service client names to their corresponding
                    client classes. The keys are values from the WSClientName enum, and
                    the values are the client classes.
    """
    map = {
        AppNames.ELASTIC_LOGGING.value: AppConfigWSClient
    }

    def __init__(self, name: AppNames):
        try:
            super().__init__(name, self.map[name.value])
        except KeyError:
            raise ValueError(f"Unsupported app name: {name}. Add to the map if needed.")





