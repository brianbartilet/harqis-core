import sys, yaml

from utilities.contracts.file import IFileLoader

class ConfigYaml(IFileLoader):
    def __init__(self, **kwargs):
        super(ConfigYaml, self).__init__(**kwargs)
        self.loader_type = kwargs.get('loader_type', yaml.FullLoader)

    def load(self) -> any:
        try:
            with open(self.file_name) as config_file:
                data = yaml.load(config_file, Loader=self.loader_type)
        except FileNotFoundError as e:
            sys.exit(f"Terminating application YAML configuration not loaded due to {e}.")

        return data