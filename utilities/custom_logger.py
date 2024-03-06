import inspect
import logging
import logging.config
import os

import yaml

from environment_variables import *


file_name = "log_config_{0}.yaml".format(ENV_TESTENV)


def custom_logger(log_level=logging.DEBUG, logger_name=None):
    if logger_name is None:
        logger_name = inspect.stack()[1][3]
    newlogger = logging.getLogger(logger_name)
    newlogger.setLevel(rootLevel)

    return newlogger


def load_logging_configuration():
    config_file_location = find_logging_config()
    with open(config_file_location) as config_file:
        config_dict = yaml.load(config_file, Loader=yaml.FullLoader)
        logging.config.dictConfig(config_dict)
    logger = logging.getLogger()

    logger.info("Loaded logging configuration from %s\n", config_file_location)
    return logger


def find_logging_config():
    cur_dir = os.getcwd()  # Dir from where search starts can be replaced with any path

    file_location = None
    while True:
        file_list = os.listdir(cur_dir)
        parent_dir = os.path.dirname(cur_dir)
        if file_name in file_list:
            print("Logging configuration file {} found in: {} ".format(file_name, cur_dir))
            file_location = os.path.join(cur_dir, file_name)
            break
        else:
            if cur_dir == parent_dir:  # if dir is root dir
                print("File not found")
                break
            else:
                cur_dir = parent_dir
    return file_location


logger = load_logging_configuration()
rootLevel = logger.getEffectiveLevel()
