"""
This module is responsible for setting up the hooks for the behave testing framework.
The hooks are set to an instance of the HooksWebDriver class.
"""

from core.testing.gherkin.behave.hooks_manager import *
from demo.testing.example_features_webdriver.references.hooks.web_driver import HooksWebDriver

# BehaveHooksManager is a class that manages hooks for the behave testing framework.
# Hooks are functions that run before or after certain events during the test execution.
# Here, we're setting the hooks attribute of the BehaveHooksManager to a list containing the HooksWebDriver class.
# HooksWebDriver is a class that defines hooks specific to the WebDriver.
BehaveHooksManager.hooks = [HooksWebDriver, ]
