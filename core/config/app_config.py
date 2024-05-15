from typing import TypeVar, Type, Any, Optional, Generic, Dict
from enum import Enum
from dataclasses import dataclass, field

# Importing configuration loader and custom logger services
from core.config.loader import ConfigLoaderService
from core.utilities.logging.custom_logger import create_logger
from core.utilities.data.qlist import QList

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


class AppConfigManager:
    """
    Manages configuration settings for an application by interfacing with a configuration loading service.

    This manager handles loading and retrieving configuration data specific to applications identified by an ID.

    Attributes:
        service (ConfigLoaderService): The service responsible for loading the application configurations.
        _current_app_configs (Optional[dict]): Dictionary to store the currently loaded application configuration. Initially set to None.
    """

    def __init__(self, service: ConfigLoaderService):
        """
        Initializes the AppConfigManager with a configuration loading service.

        Args:
            service (ConfigLoaderService): The service responsible for loading configuration data from external sources.
        """
        self.service = service
        self._current_app_configs = []  # Initially, there's no app configuration loaded.

    def load(self, app_id: str) -> None:
        """
        Loads the configuration for a specified application by its ID and stores it internally.

        Args:
            app_id (str): The identifier of the application whose configuration is to be loaded.

        Raises:
            KeyError: If no configuration is found for the specified application ID.
        """
        source = self.service.config
        if isinstance(source, dict):
            source = [{key: value} for key, value in source.items()]

        try:
            configurations = QList(source).where(lambda x: list(x.values())[0]['app_id'] == app_id)
        except KeyError:
            raise KeyError(f"Please set app_id property in config source with value {app_id}")

        if len(configurations) == 0:
            raise KeyError(f"No configurations found for app_id {app_id}")

        # Assuming a single configuration per app_id for simplicity. Adjust based on actual data structure.
        self._current_app_configs = configurations

    def get(self, loader_class: TAppConfig, config_id: str) -> dict:
        """
        Retrieves a specific configuration by its identifier from the currently loaded application configurations.

        Args:
            loader_class (TAppConfig): class model for target config
            config_id (str): The identifier for a specific configuration to retrieve.

        Returns:
            dict: The configuration dictionary corresponding to the given identifier.

        Raises:
            KeyError: If no configuration is found with the specified identifier.
        """
        try:
            target = QList(self._current_app_configs).first_or_default(lambda x: config_id in x.keys())
            return loader_class(**target[config_id])
        except TypeError as e:
            raise TypeError(f"Verify configuration setup and properties with {config_id}\nError: {e}")

