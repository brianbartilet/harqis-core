import os

from typing import TypeVar
from enum import Enum

from .types import *

T = TypeVar('T')

class Configuration(Enum):
    YAML = ConfigServiceYaml
    YML = ConfigServiceYaml
    JSON = ConfigServiceJson

class ConfigLoader:
    """ Loads a configuration from target file with support for dynamic path detection"""
    def __init__(self, loader: T, base_path=os.getcwd(), name="apps_config.yaml"):
        self.path = base_path
        self.file_name = name

        file = self.find_apps_configuration()
        self.loader = loader.value(file)

    def load(self):
        self.loader.load()

    def find_apps_configuration(self) -> str:
        cur_dir = os.path.join(self.path)
        file_location = None
        while True:
            file_list = os.listdir(cur_dir)
            parent_dir = os.path.dirname(cur_dir)
            if self.file_name in file_list:
                print("Configuration file {} found in: {} ".format(self.file_name, cur_dir))
                file_location = os.path.join(cur_dir, self.file_name)
                break
            else:
                if cur_dir == parent_dir:  # if dir is root dir
                    print("File not found")
                    break
                else:
                    cur_dir = parent_dir
        return file_location




