from typing import TypeVar, Type, Any, Optional, Generic, Dict
from enum import Enum
from dataclasses import dataclass, field

# Importing configuration loader and custom logger services
from core.config.loader import ConfigLoaderService
from core.utilities.logging.custom_logger import create_logger

TApp = TypeVar('TApp', bound=Enum)
"""
Type variable representing application names, bound to the Enum class to ensure only enumeration subclasses are used.
"""

TCfg = TypeVar('TCfg', bound=Any)
"""
Type variable for configuration objects, unrestricted in type to allow flexibility in configuration structure.
"""

TAppConfig = TypeVar('TAppConfig', bound=Any)
"""
Type variable for application configuration objects,
unrestricted in type to allow flexibility in configuration structure.
"""


@dataclass
class BaseAppConfigModel:
    """
    Base model for storing generic application configuration details.

    Attributes:
        parameters (Optional[dict]): Optional dictionary containing application-specific parameters.
        app_data (Optional[dict]): Optional dictionary for storing application context information, such as API keys.
        app_id (Optional[str]): Unique identifier for the application instance.
        id (Optional[str]): Configuration identifier, potentially used for versioning or referencing configurations.
    """
    parameters: Dict[str, Any] = field(default_factory=dict)
    app_data: Dict[str, Any] = field(default_factory=dict)
    app_id: Optional[str] = None
    id: Optional[str] = None


class AppConfig(Generic[TCfg]):
    """
    Generic class for handling application configurations using dynamic type instantiation.

    This class is designed to load and manage application configurations using a specified configuration class.

    Attributes:
        log (Logger): Logger instance for error and operation logging.
        app_config (dict): Dictionary holding the loaded configuration specific to the application.
        _config (TCfg): Instance of the configuration class loaded with the application configuration.
    """

    def __init__(self, app: TApp, type_hook_config: Type[TCfg], **kwargs):
        """
        Initialize an AppConfig instance by loading the appropriate configuration based on application enum and type.

        Args:
            app (TApp): The Enum representing the application for which configuration is loaded.
            type_hook_config (Type[TCfg]): The class type used for instantiation of the configuration object.
            **kwargs: Additional keyword arguments such as:
                      'logger' (Logger): Optional; custom logger for logging.
                      'base_path' (str): Optional; custom base path for configuration files.
        """
        self.log = kwargs.get('logger', create_logger(self.__class__.__name__))
        self.kwargs = kwargs

        try:
            self.app_config = ConfigLoaderService(**kwargs).config[app.value]
            self._config = type_hook_config(**self.app_config)  # Instantiate configuration class with loaded settings
        except KeyError as e:
            self.log.error(f"Cannot find application key for {app}: {str(e)}")
            raise

    @property
    def config(self) -> TCfg:
        """
        Retrieve the loaded configuration object instance.

        Returns:
            TCfg: The configuration instance loaded from the application-specific configuration.
        """
        return self._config
