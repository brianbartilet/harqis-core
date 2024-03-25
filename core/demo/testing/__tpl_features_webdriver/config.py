import os
from core.config.loader import ConfigFileLoader
from core.web.browser.core.config.web_driver import AppConfigWebDriver

load_config = ConfigFileLoader(file_name='__tpl_config.yaml').config

APP_NAME = os.path.basename(os.path.dirname(os.path.abspath(__file__)))
CONFIG = AppConfigWebDriver(**load_config[APP_NAME])
