from typing import TypeVar, Type, Generic
from enum import Enum

from core.config.types.json import ConfigFileJson
from core.config.types.yaml import ConfigFileYaml

TConfig = TypeVar('TConfig')


class ConfigSource(Enum):
    """
    Enum class for configuration file types.
    """
    YAML = ConfigFileYaml
    YML = ConfigFileYaml
    JSON = ConfigFileJson


class ConfigLoaderService(Generic[TConfig]):
    """
    Class to load a configuration from a target file with support for dynamic path detection.

    Attributes:
        _config (Type[IFileLoader]): The file loader to use for loading the configuration.

    Methods:
        config: Loads the configuration using the specified loader.
    """
    def __init__(self, source: ConfigSource = ConfigSource.YAML, **kwargs):
        """
        Initializes the ConfigLoader.

        Args:
            source (Type[IFileLoader]): The class of the file loader to use for loading the configuration.
            file_name (str): The name of the configuration file to load.
            base_path (str): The base path to start searching for the configuration file.
        """
        self._config = source.value(**kwargs)

    @property
    def config(self) -> TConfig:
        """
        Loads the configuration using the specified loader.

        Returns:
            The loaded configuration.
        """

        return self._config.load()

