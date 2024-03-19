import os
import json

from utilities.contracts.file import IFileLoader


class ConfigFileJson(IFileLoader):

    def __init__(self, **kwargs):
        super(ConfigFileJson, self).__init__(file_extension='.json', **kwargs)

    def load(self) -> any:
        f = {}
        try:
            with open(self.full_path_to_file) as config_file:
                f = json.load(config_file)
        except FileNotFoundError as e:
            self.log.error(f"JSON configuration not loaded due to {e}.")

        return f
