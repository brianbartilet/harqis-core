import os
import inspect
import re
import subprocess

from core.config.constants.environment import EnvSettings


# region Environment Variables Helpers

def get_env_variable_name(env):
    """
    Function to get the name of an environment variable.
    It uses regex to find the variable name from the line where this function is called.
    The 'ENV_' prefix is removed from the variable name.

    Args:
        env: The environment variable.

    Returns:
        The name of the environment variable without the 'ENV_' prefix.
    """
    for line in inspect.getframeinfo(inspect.currentframe().f_back)[3]:
        name = re.search(r'\bget_env_variable_name\s*\(\s*([A-Za-z_][A-Za-z0-9_]*)\s*\)*', line)
        if name:
            return re.sub('^ENV_', '', name.group(1))


def set_env_variable_value(env, value):
    """
    Function to set the value of an environment variable.
    It uses regex to find the variable name from the line where this function is called.
    The 'ENV_' prefix is removed from the variable name.
    If the variable name is found, its value is set in the environment.
    If the variable name is not found, an exception is raised.

    Args:
        env: The environment variable.
        value: The value to set for the environment variable.

    Raises:
        Exception: No environment variable was found.
    """
    env_variable = None
    for line in inspect.getframeinfo(inspect.currentframe().f_back)[3]:
        name = re.search(r'\bset_env_variable_value\s*\(\s*([A-Za-z_][A-Za-z0-9_]*)\s*\)*', line)
        if name:
            env_variable = re.sub('^ENV_', '', name.group(1))

    if env_variable is not None:
        os.environ[env_variable] = value
    else:
        raise Exception('Environment variable was not set')


def get_env_variable_value(env):
    """
    Function to get the value of an environment variable.
    It uses regex to find the variable name from the line where this function is called.
    The 'ENV_' prefix is removed from the variable name.
    If the variable name is found, its value is returned from the environment.
    If the variable name is not found, an exception is raised.

    Args:
        env: The environment variable.

    Returns:
        The value of the environment variable.

    Raises:
        Exception: If the environment variable was not found.
    """
    env_variable = None
    for line in inspect.getframeinfo(inspect.currentframe().f_back)[3]:
        name = re.search(r'\bget_env_variable_value\s*\(\s*([A-Za-z_][A-Za-z0-9_]*)\s*\)*', line)
        if name:
            env_variable = re.sub('^ENV_', '', name.group(1))

    if env_variable is not None:
        return os.environ.get(env_variable)
    else:
        raise Exception('Environment variable was not set')


def get_git_root(path):
    """
    Function to get the root directory of a git repository.

    Args:
        path (str): The path where to start searching for the git root.

    Returns:
        The root directory of the git repository.
    """
    git_root = subprocess.check_output(['git', 'rev-parse', '--show-toplevel'], cwd=path)
    return git_root.decode('utf-8').strip()

# endregion


#  region Default Environment Variables

# Environment setting, default is development environment
ENV = os.environ.get("ENV", EnvSettings.DEV.value)

# Debug setting, default is '1'
ENV_DEBUG = os.environ.get("DEBUG", '1')

# Path setting
ENV_PATH = os.environ.get("PATH", None)

# Current user profile, default is None
ENV_CURRENT_USER_PROFILE = os.environ.get("USERPROFILE", None)

# Enable proxies, default is False
ENV_ENABLE_PROXY = os.environ.get("ENABLE_PROXY", False)

# Path to the application configuration, default is the current working directory
ENV_APP_CONFIG = os.environ.get("ENV_PATH_APP_CONFIG", "apps_config.yaml")

# Root directory of the application, default is the root directory of the repository, unless specified
ENV_ROOT_DIRECTORY = os.environ.get('ENV_ROOT_DIRECTORY', get_git_root(os.path.dirname(os.path.abspath(__file__))))

# Local application data path, default is None
ENV_LOCAL_APP_DATA = os.environ.get("LOCALAPPDATA", None)

# Tasks mapping for workflows defaults to testing tasks key
ENV_TASK_APP = os.environ.get("ENV_TASK_APP", 'MAP_TESTING_TASKS')

#  endregion

