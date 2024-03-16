import yaml
import os

from utilities.contracts.file import IFileLoader


class ConfigYaml(IFileLoader):
    def __init__(self, **kwargs):
        super(ConfigYaml, self).__init__(**kwargs, file_extension='.yaml')
        self.loader_type = kwargs.get('loader_type', yaml.FullLoader)

    def load(self) -> any:
        data = {}
        try:
            with open(self.full_path_to_file) as config_file:
                data = yaml.load(config_file, Loader=self.loader_type)
        except FileNotFoundError as e:
            self.log.error(f"YAML configuration not loaded due to {e}.")

        return data
