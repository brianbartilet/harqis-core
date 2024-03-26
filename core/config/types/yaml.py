import yaml
import os
from core.utilities.contracts.file import IFileLoader


class ConfigFileYaml(IFileLoader):
    def __init__(self, **kwargs):
        super(ConfigFileYaml, self).__init__(**kwargs, file_extension='.yaml')
        self.loader_type = kwargs.get('loader_type', yaml.FullLoader)
        self.env_replace = kwargs.get('env_replace', True)

    def load(self) -> any:
        data = {}
        try:
            with open(self.full_path_to_file) as config_file:
                data = yaml.load(config_file, Loader=self.loader_type)

                # Recursively update placeholders with environment variables
                def replace_env_variables(config_item):
                    if isinstance(config_item, dict):
                        for key, value in config_item.items():
                            config_item[key] = replace_env_variables(value)
                    elif isinstance(config_item, str):
                        # Replace placeholder with environment variable value if it exists
                        if config_item.startswith('${') and config_item.endswith('}'):
                            env_var = config_item[2:-1]  # Extract the name of the environment variable
                            return os.getenv(env_var, config_item)  # Default to original string if not found
                    return config_item

                if self.env_replace:
                    return replace_env_variables(data)
                else:
                    return data

        except FileNotFoundError as e:
            self.log.error(f"YAML configuration not loaded due to {e}.")

        return data
