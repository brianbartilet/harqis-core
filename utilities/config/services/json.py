import sys, json

from .base import ConfigService

class ConfigServiceJson(ConfigService):
    def load(self) -> object:
        try:
            config_file_location = self.file_path
            with open(config_file_location) as config_file:
                config_dict = json.load(config_file)
        except Exception as e:
            sys.exit("Terminating application JSON configuration not loaded due to {0}.".format(e))

        return config_dict