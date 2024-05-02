from typing import *
from selenium.webdriver.remote.webelement import WebElement as SeleniumWebElement
from selenium.webdriver.common.by import By as SeleniumBy
from selenium.webdriver.common.keys import Keys as SeleniumKeys
from selenium.common import exceptions as SeleniumExceptions

from playwright.async_api import ElementHandle as PlaywrightElementHandle, Locator as PlaywrightLocator, Keyboard as PlaywrightKeyboard, Error as PlaywrightError

# TypeVars are more useful for generic classes and functions
TElement = Union[SeleniumWebElement, PlaywrightElementHandle]
TLocator = Union[SeleniumBy, PlaywrightLocator]
TKeyboard = Union[SeleniumKeys, PlaywrightKeyboard]
TException = Union[SeleniumExceptions.WebDriverException, PlaywrightError]
