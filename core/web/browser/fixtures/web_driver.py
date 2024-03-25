from typing import TypeVar, Generic

from core.web.browser.core.config.web_driver import AppConfigWebDriver

from core.web.browser.core.constants.drivers import WebDriverNames
from core.web.browser.core.driver.selenium import DriverSelenium
from core.web.browser.core.driver.playwright import DriverPlaywright
from core.web.browser.core.driver.puppeteer import DriverPuppeter

from core.web.browser.core.constants.browsers import BrowserNames
from core.web.browser.core.browser.chrome import BrowserChrome
from core.web.browser.core.browser.firefox import BrowserFirefox
from core.web.browser.core.browser.edge import BrowserEdge


TFixture = TypeVar("TFixture")


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


class BrowserTypeClass:
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


class WebDriver(Generic[TFixture]):

    def __init__(self, config: AppConfigWebDriver, **kwargs):
        self._config = config
        self._driver = WebDriverClass.map[config.type](**config.parameters)
        self._browser = BrowserTypeClass.map[config.browser](**config.parameters)

        self.kwargs = kwargs
