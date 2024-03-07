import sys
import yaml, json

from typing import Type
from environment_variables import *


class ConfigLoader:
    """ Loads a configuration from target file with support for dynamic path detection"""

    def __init__(self, base_path=ENV_PATH_APP_CONFIG, name="apps_config_{0}.{1}".format(ENV_TESTENV, 'yaml'),):
        """
        Initializes a ConfigLoader then load to a target dto
        """
        self.path = base_path
        self.file_name = name

    def load(self):
        if self.file_name.endswith('.json'):
            return self.load_json()
        elif self.file_name.endswith('.yaml') or self.file_name.endswith('.yml'):
            return self.load_yaml()
        else:
            raise ValueError("Unsupported file format.")

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
    def load_yaml(self) -> object:
        try:
            config_file_location = self.find_apps_configuration()
            with open(config_file_location) as config_file:
                config_dict = yaml.load(config_file, Loader=yaml.FullLoader)
                config_dict[ENV_CURRENT_CONFIGURATION_FILE_PATH] = config_file_location
        except Exception as e:
            sys.exit("Terminating application YAML configuration not loaded due to {0}.".format(e))


        return config_dict

    def load_json(self) -> object:
        try:
            config_file_location = self.find_apps_configuration()
            with open(config_file_location) as config_file:
                config_dict = json.load(config_file)
                config_dict[ENV_CURRENT_CONFIGURATION_FILE_PATH] = config_file_location
        except Exception as e:
            sys.exit("Terminating application JSON configuration not loaded due to {0}.".format(e))

        return config_dict





