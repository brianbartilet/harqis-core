import os
from typing import Dict
from abc import ABC, abstractmethod
from core.utilities.logging.custom_logger import create_logger


class IGenerator(ABC):
    def __init__(self, source: str, *args, **kwargs):
        self.log = create_logger(self.__class__.__name__)
        self.source: str = source
        self.file_name: str = ''
        self.files: Dict[str, str] = {}  # key: file_path, value: content
        self.directories: Dict[str, str] = {}
        self.templates: Dict[str, str] = {}

    @abstractmethod
    def initialize_directories(self, base_path: str) -> None:
        ...

    @abstractmethod
    def initialize_templates(self) -> None:
        ...

    @abstractmethod
    def load_source(self) -> dict:
        ...

    @abstractmethod
    def create_directories(self) -> None:
        """
        Create the directories from the directories dictionary
        """
        for directory in self.directories.values():
            if not os.path.exists(directory):
                os.makedirs(directory)

    @abstractmethod
    def parse_spec(self, source_data: dict) -> None:
        ...

    @abstractmethod
    def write_files(self, **kwargs) -> None:
        except_keys = kwargs.get('except_keys', [])

        for key in self.files.keys():
            with open(key, 'w') as file:
                file.write(self.files[key])
        for key in self.directories.keys():
            if key in except_keys:
                continue
            file_path = os.path.join(self.directories[key], '__init__.py')
            with open(file_path, 'w') as file:
                pass
