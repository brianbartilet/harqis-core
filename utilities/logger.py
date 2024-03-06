import inspect
import logging
import logging.config
import os

import yaml

def create_custom_logger(logger_name=None):
    if logger_name is None:
        logger_name = inspect.stack()[1][3]
    new_logger = logging.getLogger(logger_name)
    new_logger.setLevel(rootLevel)
    return new_logger


def load_logging_configuration():
    config_file_location = find_logging_config()
    with open(config_file_location) as config_file:
        config_dict = yaml.load(config_file)
        logging.config.dictConfig(config_dict)
    logger = logging.getLogger()

    logger.info("Loaded logging configuration from %s", config_file_location)

    return logger


def find_logging_config():
    cur_dir = os.getcwd()  # Dir from where search starts can be replaced with any path

    file_location = None
    while True:
        file_list = os.listdir(cur_dir)
        parent_dir = os.path.dirname(cur_dir)
        if file_name in file_list:
            print("File Exists in: {} ".format(cur_dir))
            file_location = os.path.join(cur_dir, file_name)
            break
        else:
            if cur_dir == parent_dir:  # if dir is root dir
                print("File not found")
                break
            else:
                cur_dir = parent_dir
    return file_location

file_name = "log_config.yaml" #file to be searched
logger = load_logging_configuration()
rootLevel = logger.getEffectiveLevel()
