import sys, yaml

from .base import ConfigService

class ConfigServiceYaml(ConfigService):
    def load(self) -> object:
        try:
            with open(self.file_path) as config_file:
                config_dict = yaml.load(config_file, Loader=yaml.FullLoader)
        except Exception as e:
            sys.exit("Terminating application YAML configuration not loaded due to {0}.".format(e))

        return config_dict