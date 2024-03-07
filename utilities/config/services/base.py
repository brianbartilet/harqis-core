from abc import ABC, abstractmethod

class ConfigService(ABC):
    def __init__(self, file_path: str):
        self.file_path = file_path

    @abstractmethod
    def load(self) -> any:
        ...
