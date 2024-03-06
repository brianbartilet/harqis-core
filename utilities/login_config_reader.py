import os
import sys

import yaml


class LoginConfigReader():

    def __init__(self, app=None, testenv=None):
        if app is None:
            app = os.environ.get("APP")
        if testenv is None:
            testenv = os.environ.get("TESTENV")
        self.app = app
        self.testenv = testenv
        self.config_file = None


    def get_value(self, filename : str, value : str):
        try:
            if self.config_file is None:
                self._load_config_file_data()

            loginset = self.config_file.get(filename)
            if loginset is None:
                dataval = self.get_value('DEFAULT', value)
            else:
                dataval = loginset.get(value)
                if dataval is None:
                    dataval = self.get_value('DEFAULT', value)
            return dataval
        except:
            sys.exit("Failed to read from configuration reader: \n"
                     + "FILE: " + filename + " VALUE: " + value)

    def _load_config_file_data(self):
        filepath = os.path.join(os.getcwd(), "Application", self.app, "datafiles", self.testenv, "logincfg.yaml")
        with open(filepath, 'r') as ymlfile:
            self.config_file = yaml.load(ymlfile)