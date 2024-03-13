import os
from typing import TypeVar, Type
from enum import Enum

T = TypeVar('T')

from .types import *


class Configuration(Enum):
    YAML = ConfigYaml
    YML = ConfigYaml
    JSON = ConfigJson


class ConfigLoader:
    """
    Loads a configuration from a target file with support for dynamic path detection.
    """
    def __init__(self, file: Configuration = Configuration.YAML, file_name: str = "apps_config.yaml", base_path: str = os.getcwd()):
        """
        Initializes the ConfigLoader.

        Args:
            file (Type[IFileLoader]): The class of the file loader to use for loading the configuration.
            file_name (str): The name of the configuration file to load.
            base_path (str): The base path to start searching for the configuration file.
        """
        self._config = file.value(file_name=file_name, base_path=base_path)

    @property
    def config(self) -> T:
        """
        Loads the configuration using the specified loader.

        Returns:
            The loaded configuration.
        """
        file_path = self._config.find_file_from_base_path()
        if file_path is None:
            raise FileNotFoundError(f"Configuration file {self._config.file_name} not found in "
                                    f"{self._config.base_path} or its parent directories.")

        return self._config.load()
