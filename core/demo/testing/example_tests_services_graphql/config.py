"""
This module is responsible for loading configuration settings for a specific application
from a YAML configuration file and initializing an application-specific web service client configuration.

It leverages a configuration loader to read settings and dynamically assigns these settings
based on the application's directory name. This allows for flexible configuration management
that adapts to the application's deployment environment.

Attributes:
    APP_NAME (str): The name of the application, derived from the directory name of the current file.
                    This is used to select the appropriate configuration section from the YAML file.
    CONFIG (AppConfigWSClient): A configured instance of AppConfigWSClient containing web service
                                connection settings specific to the application determined by APP_NAME.
"""
import os
from core.config.loader import ConfigLoaderService
from core.web.services.core.config.webservice import AppConfigWSClient

# Load configuration from a YAML file using the ConfigFileLoader class.
# The 'file_name' parameter specifies the name of the YAML configuration file.
load_config = ConfigLoaderService(file_name='sample_config.yaml').config

# Determine the application name by extracting the base name of the directory
# where the current script is located. This is used to segment the configuration
# specific to this application within the YAML file.
APP_NAME = os.path.basename(os.path.dirname(os.path.abspath(__file__)))

# with the specific configuration for this application, fetched by keying into
# the 'load_config' dictionary with 'APP_NAME'.
CONFIG = AppConfigWSClient(**load_config[APP_NAME])
