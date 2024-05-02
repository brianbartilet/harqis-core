import os
from core.config.loader import ConfigLoaderService
from core.web.browser.core.config.web_driver import AppConfigWebDriver

"""
This script is designed to load configuration settings for a specific application from a YAML file,
using the application's directory name as a key to retrieve appropriate configurations. These configurations
are then used to initialize a web driver configuration object for the application.

The script utilizes the `ConfigFileLoader` for loading configurations and `AppConfigWebDriver` to apply these
configurations to a web driver instance.
"""

# Load configurations from a specified YAML file.
load_config = ConfigLoaderService(file_name='sample_config.yaml').config

# Determine the application's name based on the directory name where this script is located.
APP_NAME = os.path.basename(os.path.dirname(os.path.abspath(__file__)))

# Initialize the application configuration for a web driver using settings from the loaded configuration.
CONFIG = AppConfigWebDriver(**load_config[APP_NAME])
