import os
from typing import TypeVar, Type, Any, Generic
from enum import Enum

from core.config.loader import ConfigFileLoader
from core.utilities.logging.custom_logger import create_logger
from core.config.environment_variables import ENV_ROOT_DIRECTORY

TApp = TypeVar('TApp', bound=Enum)
"""
TypeVar for application names, bound to the Enum class.
This restricts the TApp type variable to only Enum subclasses,
ensuring that app names are defined as enumerations.
"""

TCfg = TypeVar('TCfg', bound=Any)
"""
TypeVar for configuration classes.
The bound=Any allows TCfg to be any type,
but in practice, it is expected to be a class that can be instantiated
with keyword arguments from a configuration dictionary.
"""


class AppConfig(Generic[TCfg]):
    """
    A class for loading and accessing application configuration.

    This class is generic with respect to ConfigClass, allowing it to work
    with any configuration class that can be instantiated from a dictionary.

    Attributes:
        log (Logger): A logger instance for logging error messages.
        base_path (str): The base path where the configuration file is located.
        app_config (dict): The loaded configuration for the specified application.
        _config (ConfigClass): An instance of the configuration class initialized with the loaded configuration.

    Raises:
        KeyError: If the specified application key is not found in the configuration file.
    """
    def __init__(self, app: TApp, type_hook_config: Type[TCfg], **kwargs):
        """
        Initializes the AppConfig instance.

        Args:
            app (AppName): The name of the application for which to load the configuration.
            type_hook_config (Type[ConfigClass]): The class to be used for creating the configuration instance.
            **kwargs: Optional keyword arguments. Can include 'logger' for a custom logger and 'base_path' for a custom configuration file path.
        """
        self.log = kwargs.get('logger', create_logger(self.__class__.__name__))

        try:
            self.app_config = ConfigFileLoader(**kwargs).config[app.value]
            self._config = type_hook_config(**self.app_config)  # Instantiate ConfigClass
        except KeyError:
            self.log.error(f"Cannot find application key for {app}.")
            raise KeyError

    @property
    def config(self) -> TCfg:
        """
        Returns the configuration instance.

        Returns:
            ConfigClass: An instance of the configuration class initialized with the loaded configuration.
        """
        return self._config
