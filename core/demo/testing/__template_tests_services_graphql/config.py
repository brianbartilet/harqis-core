import os
from core.config.loader import ConfigFileLoader
from core.web.services.core.config.webservice import AppConfigWSClient

load_config = ConfigFileLoader().config

APP_NAME = os.path.basename(os.path.dirname(os.path.abspath(__file__)))
CONFIG = AppConfigWSClient(**load_config[APP_NAME])
