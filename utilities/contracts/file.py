import os
from abc import ABC, abstractmethod
from typing import TypeVar, Generic, Optional
from pathlib import Path

T = TypeVar('T')

class IFileLoader(ABC, Generic[T]):
    def __init__(self, file_name: str, base_path: str = os.getcwd(), **kwargs) -> None:
        self.file_name = file_name
        self.base_path = Path(base_path)

    @abstractmethod
    def load(self) -> any:
        """
        Loads the file content using the specified loader.

        Returns:
            The loaded content of the file.
        """
        ...

    def find_file_from_base_path(self) -> Optional[Path]:
        """
        Searches for the file in the directory tree starting from the base path.

        Returns:
            The path to the file if found, otherwise None.
        """
        for parent in [self.base_path, *self.base_path.parents]:
            potential_path = parent / self.file_name
            if potential_path.exists():
                print(f"Configuration file {self.file_name} found in: {parent}")
                return potential_path
        print("File not found")

        return None