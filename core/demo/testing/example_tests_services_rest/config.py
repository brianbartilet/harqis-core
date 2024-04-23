import os
from core.config.loader import ConfigFileLoader
from core.web.services.core.config.webservice import AppConfigWSClient

# Load configuration from a YAML file using the ConfigFileLoader class.
# The 'file_name' parameter specifies the name of the YAML configuration file.
load_config = ConfigFileLoader(file_name='sample_config.yaml').config

# Determine the application name by extracting the base name of the directory
# where the current script is located. This is used to segment the configuration
# specific to this application within the YAML file.
APP_NAME = os.path.basename(os.path.dirname(os.path.abspath(__file__)))

# Create a configuration client for the web service. This client is initialized
# with the specific configuration for this application, fetched by keying into
# the 'load_config' dictionary with 'APP_NAME'.
CONFIG = AppConfigWSClient(**load_config[APP_NAME])
