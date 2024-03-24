from abc import abstractmethod
from typing import TypeVar, Generic, Type

from core.web.browser.core.constants.drivers import WebDriverNames

from core.web.browser.core.config.web_driver import AppConfigWebDriver

from core.web.browser.core.driver.selenium import DriverSelenium
from core.web.browser.core.driver.playwright import DriverPlaywright
from core.web.browser.core.driver.puppeteer import DriverPuppeter

from core.utilities.asserts.helper import LoggedAssertHelper

TFixture = TypeVar("TFixture")
TResponse = TypeVar("TResponse")


class WebDriverClass:
    """
    A class that maps web driver names to their corresponding client classes.

    Attributes:
        map (dict): A dictionary mapping web service client names to their corresponding
                    client classes. The keys are values from the WebDriverNames enum, and
                    the values are the driver classes.
    """
    map = {
        WebDriverNames.SELENIUM.value: DriverSelenium,
        WebDriverNames.PUPPETEER.value: DriverPuppeter,
        WebDriverNames.PLAYWRIGHT.value: DriverPlaywright,

    }


class IFixturePageObjectModel(Generic[TFixture]):

    def __init__(self, config: AppConfigWebDriver, **kwargs):
        self._config = config
        self.kwargs = kwargs

