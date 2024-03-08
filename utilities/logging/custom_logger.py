import os
import inspect
import logging
import logging.config
import yaml

file_name = "logging.yaml"


def custom_logger(logger_name=None):
    """
    Create a custom logger with the specified name or the name of the calling function.

    :param logger_name: Optional; the name of the logger. If not provided, the name of the calling function is used.
    :return: A logger object with the specified name.
    """
    if logger_name is None:
        logger_name = inspect.stack()[1][3]
    new_logger = logging.getLogger(logger_name)
    new_logger.setLevel(rootLevel)

    return new_logger


def load_logging_configuration():
    """
    Load logging configuration from a YAML file and configure the logging module.

    :return: The root logger object after loading the configuration.
    """
    config_file_location = find_logging_config()
    with open(config_file_location) as config_file:
        config_dict = yaml.load(config_file, Loader=yaml.FullLoader)
        logging.config.dictConfig(config_dict)
    new_logger = logging.getLogger()

    new_logger.info("Loaded logging configuration from %s\n", config_file_location)
    return new_logger


def find_logging_config():
    """
    Search for the logging configuration file (logging.yaml) starting from the current working directory and moving up the directory tree.

    :return: The file path of the logging configuration file if found, otherwise None.
    """
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
