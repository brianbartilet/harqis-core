import sys, json

from utilities.contracts.file import IFileLoader


class ConfigJson(IFileLoader):

    def __init__(self, **kwargs):
        super(ConfigJson, self).__init__(**kwargs)

    def load(self) -> any:
        try:
            config_file_location = self.file_name
            with open(config_file_location) as config_file:
                f = json.load(config_file)
        except FileNotFoundError as e:
            sys.exit(f"Terminating application JSON configuration not loaded due to {e}.")

        return f