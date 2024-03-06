import os
import inspect, re
from importlib import reload

from settings import *


#  region Default Environment Variables

ENV_ENABLE_PROXY = os.environ.get("ENABLE_PROXY", False)
ENV_TESTENV = os.environ.get("ENV", SettingsEnvironment.DEV.value)
ENV_PATH_APP_CONFIG = os.environ.get("ENV_PATH_APP_CONFIG", None)
ENV_ROOT_DIRECTORY = os.environ.get('ENV_APP_PATH', os.path.dirname(os.path.abspath(__file__)))
ENV_TASK_APP = os.environ.get("ENV_TASK_APP", 'DAILY_TASKS')
ENV_CURRENT_USER_PROFILE = os.environ.get("USERPROFILE", None)
ENV_LOCAL_APP_DATA = os.environ.get("LOCALAPPDATA", None)
ENV_DEBUG = os.environ.get("DEBUG", '1')
ENV_PATH = os.environ.get("PATH")

#  endregion


def get_env_variable_name(env):
    for line in inspect.getframeinfo(inspect.currentframe().f_back)[3]:
        name = re.search(r'\bget_env_variable_name\s*\(\s*([A-Za-z_][A-Za-z0-9_]*)\s*\)*', line)
        if name:
            return re.sub('^ENV_', '', name.group(1))


def set_env_variable_value(env, value):
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
    env_variable = None
    for line in inspect.getframeinfo(inspect.currentframe().f_back)[3]:
        name = re.search(r'\bget_env_variable_value\s*\(\s*([A-Za-z_][A-Za-z0-9_]*)\s*\)*', line)
        if name:
            env_variable = re.sub('^ENV_', '', name.group(1))

    if env_variable is not None:
        return os.environ.get(env_variable)
    else:
        raise Exception('Environment variable was not set')