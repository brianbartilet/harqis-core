import os
from typing import Type
from enum import Enum

from utilities.resources.types import *

TData = TypeVar('TData')


class Resource(Enum):
    JSON = ResourceFileJson
    GQL = ResourceFileGql


class ResourceDataLoader:
    """
    Loads data from a target file with support for dynamic path detection.
    """
    def __init__(self, resource: Resource, file_name: str, base_path: str = os.getcwd(), **kwargs):
        """
        Initializes the ConfigLoader.

        Args:
            resource (Type[IFileLoader]): The class of the file loader to use for loading the configuration.
            file_name (str): The name of the configuration file to load.
            base_path (str): The base path to start searching for the configuration file.
        """
        if not file_name.endswith('.gql'):
            file_name += '.gql'
        self.file_name = file_name

        self._resource = resource.value(file_name=file_name, base_path=base_path, **kwargs)

    @property
    def data(self) -> TData:
        """
        Loads the data of target using the specified resource type.

        Returns:
            The loaded json
        """
        return self._resource.load()