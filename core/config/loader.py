import os
from typing import TypeVar, Type, Generic
from enum import Enum

from core.config.types.json import ConfigFileJson
from core.config.types.yaml import ConfigFileYaml

TConfig = TypeVar('TConfig')


class ConfigFile(Enum):
    """
    Enum class for configuration file types.
    """
    YAML = ConfigFileYaml
    YML = ConfigFileYaml
    JSON = ConfigFileJson


class ConfigFileLoader(Generic[TConfig]):
    """
    Class to load a configuration from a target file with support for dynamic path detection.

    Attributes:
        _config (Type[IFileLoader]): The file loader to use for loading the configuration.

    Methods:
        config: Loads the configuration using the specified loader.
    """
    def __init__(self,
                 file: ConfigFile = ConfigFile.YAML,
                 file_name="apps_config.yaml",
                 base_path: str = os.getcwd()):
        """
        Initializes the ConfigLoader.

        Args:
            file (Type[IFileLoader]): The class of the file loader to use for loading the configuration.
            file_name (str): The name of the configuration file to load.
            base_path (str): The base path to start searching for the configuration file.
        """
        self._config = file.value(file_name=file_name, base_path=base_path)

    @property
    def config(self) -> TConfig:
        """
        Loads the configuration using the specified loader.

        Returns:
            The loaded configuration.

        Raises:
            FileNotFoundError: If the configuration file is not found in the base path or its parent directories.
        """
        file_path = self._config.find_file_from_base_path()
        if file_path is None:
            raise FileNotFoundError(f"Configuration file {self._config.file_name} not found in "
                                    f"{self._config.base_path} or its parent directories.")

        return self._config.load()

