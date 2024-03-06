import yaml
from environment_variables import *
import sys

ENV_CURRENT_CONFIGURATION_FILE_PATH = 'CURRENT_CONFIGURATION_FILE_PATH'


class ConfigurationLoader:

    def __init__(self, **kwargs):
        self.file_name = kwargs.get('configuration_file', "apps_config_{0}.yaml"
                                    .format(ENV_TESTENV).lower())
        self.path = kwargs.get('path', ENV_PATH_APP_CONFIG)

    def load_app_configuration(self):

        try:
            config_file_location = self.find_apps_configuration()
            with open(config_file_location) as config_file:
                config_dict = yaml.load(config_file, Loader=yaml.FullLoader)
                config_dict[ENV_CURRENT_CONFIGURATION_FILE_PATH] = config_file_location
        except Exception as e:
            sys.exit("Terminating application configuration not loaded due to {0}.".format(e))

        return config_dict

    def find_apps_configuration(self):
        cur_dir = os.path.join(self.path)
        file_location = None
        while True:
            file_list = os.listdir(cur_dir)
            parent_dir = os.path.dirname(cur_dir)
            if self.file_name in file_list:
                print("Applications configuration file {} found in: {} ".format(self.file_name, cur_dir))
                file_location = os.path.join(cur_dir, self.file_name)
                break
            else:
                if cur_dir == parent_dir:  # if dir is root dir
                    print("File not found")
                    break
                else:
                    cur_dir = parent_dir
        return file_location





