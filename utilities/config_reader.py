import os
import yaml


class ConfigReader:

    def __init__(self, target_application : str, **kwargs):
        self.app = target_application
        self.config_file = None

    def get_value_for(self, env, param):
        if self.config_file is None:
           self._load_config_file_data()
        value = self.config_file[env][param]
        return value

    def _load_config_file_data(self):
        filepath = os.path.join(os.getcwd(), "Application", self.app , "configfiles", "env_config.yaml")
        with open(filepath, 'r') as ymlfile:
            self.config_file = yaml.load(ymlfile)
