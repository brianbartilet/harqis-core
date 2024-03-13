import json

from contracts.file import IFileLoader


class ConfigJson(IFileLoader):

    def __init__(self, **kwargs):
        super(ConfigJson, self).__init__(**kwargs)

    def load(self) -> any:
        f = {}
        try:
            config_file_location = self.file_name
            with open(config_file_location) as config_file:
                f = json.load(config_file)
        except FileNotFoundError as e:
            self.log.error(f"JSON configuration not loaded due to {e}.")

        return f