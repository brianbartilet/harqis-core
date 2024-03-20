import os
from abc import ABC, abstractmethod
from typing import TypeVar, Generic, Optional
from pathlib import Path

from utilities.logging.custom_logger import create_logger


TFile = TypeVar('TFile')


class IFileLoader(ABC, Generic[TFile]):
    """
    Abstract base class for a file loader.

    This class defines the interface for a file loader, which is responsible for loading the content of a file.
    The type of the loaded content is defined by the generic parameter T.

    Attributes:
        log: A logger instance used for logging.
        file_name: The name of the file to load.
        base_path: The base path where to start searching for the file.
        file_extension: The expected file extension. If provided, it will be appended to the file name if not already present.
    """

    def __init__(self, file_name: str, base_path: str = None, **kwargs) -> None:
        """
        Initializes a new instance of the IFileLoader class.

        Args:
            file_name: The name of the file to load.
            base_path: The base path where to start searching for the file. Defaults to the current working directory.
            **kwargs: Optional keyword arguments. Supported arguments are 'logger' and 'file_extension'.
        """

        self.log = kwargs.get('logger', create_logger(self.__class__.__name__))

        self.file_name = file_name
        self.base_path = Path(os.getcwd() if base_path is None else base_path)

        self.file_extension = kwargs.get('file_extension', None)
        if self.file_extension:
            if not file_name.endswith(self.file_extension):
                self.file_name += self.file_extension

        self.full_path_to_file = self.find_file_from_base_path()
        if self.full_path_to_file is None:
            raise FileNotFoundError(f"File {self.file_name} not found in "
                                    f"{self.base_path} or its parent directories.")

    @abstractmethod
    def load(self) -> any:
        """
        Abstract method to load the file content.

        This method should be overridden by subclasses to provide the specific loading logic.

        Returns:
            The loaded content of the file.
        """
        ...

    def find_file_from_base_path(self) -> Optional[Path]:
        """
        Searches for the file in the directory tree starting from the base path.

        This method traverses the directory tree starting from the base path and moving up to the parent directories.
        It stops when it finds a file that matches the file name and returns its path.

        Returns:
            The path to the file if found, otherwise None.
        """
        for parent in [self.base_path, *self.base_path.parents]:
            potential_path = parent / self.file_name
            if potential_path.exists():
                print(f"File {self.file_name} found in: {parent}")
                return potential_path
