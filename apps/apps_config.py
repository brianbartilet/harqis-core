from enum import Enum
from web.services.core.config.webservice import AppConfigWSClient
from config.app_config import AppConfig
from typing import TypeVar, Generic

TConfig = TypeVar("TConfig")


class AppNames(Enum):
    """
    Enum class for environment settings.

    Attributes:
        API_GPT (str): ChatGPT integration.
        TASKS_CLIENT (str): Celery tasks client.
    """
    API_GPT = 'HARQIS_GPT'
    TASKS_CLIENT = 'CELERY_TASKS'


class AppConfigLoader(AppConfig):
    """
    A class that maps web service client names to their corresponding client classes.

    Attributes:
        map (dict): A dictionary mapping web service client names to their corresponding
                    client classes. The keys are values from the WSClientName enum, and
                    the values are the client classes.
    """
    map = {
        AppNames.API_GPT.value: AppConfigWSClient

    }

    def __init__(self, name: AppNames):
        super().__init__(name, self.map[name.value])





