import os
import inspect
import logging
import logging.config
import yaml

file_name = "logging.yaml"


def create_logger(logger_name=None):
    """
    Create a custom logger with the specified name or the name of the calling function.

    Args:
        logger_name: Optional; the name of the logger. If not provided, the name of the calling function is used.

    Returns:
        A logger object with the specified name.
    """
    if logger_name is None:
        logger_name = inspect.stack()[1][3]
    new_logger = logging.getLogger(logger_name)
    new_logger.setLevel(rootLevel)

    return new_logger


def load_logging_configuration():
    """
    Load logging configuration from a YAML file and configure the logging module.

    Returns:
        The root logger object after loading the configuration.
    """
    config_file_location = find_logging_config()
    if config_file_location is None:
        raise NotImplementedError(f"Please add a logging file {file_name} in root directory.")
    try:
        with open(config_file_location) as config_file:
            config_dict = yaml.load(config_file, Loader=yaml.FullLoader)
            logging.config.dictConfig(config_dict)
    except FileNotFoundError:
        raise FileNotFoundError(f"Logging configuration file not found: {config_file_location}")

    new_logger = logging.getLogger()

    new_logger.info("Loaded logging configuration from %s\n", config_file_location)

    return new_logger


def find_logging_config():
    """
    Search for the logging configuration file (logging.yaml).

    Priority 1: walks up from the current working directory to find a project-level config.
    Priority 2: falls back to the bundled logging.yaml inside the installed core package.

    Returns:
        The file path of the logging configuration file if found, otherwise None.
    """
    cur_dir = os.getcwd()
    while True:
        if file_name in os.listdir(cur_dir):
            return os.path.join(cur_dir, file_name)
        parent_dir = os.path.dirname(cur_dir)
        if cur_dir == parent_dir:
            break
        cur_dir = parent_dir

    # Fallback: bundled logging.yaml shipped with the core package (core/logging.yaml)
    core_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    bundled = os.path.join(core_dir, file_name)
    if os.path.isfile(bundled):
        return bundled

    return None


logger = load_logging_configuration()
rootLevel = logger.getEffectiveLevel()
