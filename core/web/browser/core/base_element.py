
import time
import os

from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.common.exceptions import *

from behave.runner import Context



future_speed = os.getenv("FUTURE_SPEED", "N").lower()

def find_element(locator: By, locator_value: str, suppress_errors=False):
    def decorator(func):
        def wrapper(*args):
            if suppress_errors:
                try:
                    return args[0].driver.find_element(locator, locator_value)
                except NoSuchElementException:
                    return None
            else:
                return args[0].driver.find_element(locator, locator_value)
        return wrapper
    return decorator


def find_elements(locator: By, locator_value: str):
    def decorator(func):
        def wrapper(*args) -> []:
            return args[0].driver.find_elements(locator, locator_value)
        return wrapper
    return decorator
