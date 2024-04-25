from typing import TypeVar, Generic

from core.web.browser.core.contracts.driver import IWebDriver, TWebDriver
from core.web.browser.core.contracts.browser import IBrowser, TBrowser
from core.web.browser.core.config.web_driver import AppConfigWebDriver

from core.web.browser.core.constants.drivers import WebDriverNames
from core.web.browser.core.driver.selenium import DriverSelenium
from core.web.browser.core.driver.playwright import DriverPlaywright
from core.web.browser.core.driver.puppeteer import DriverPuppeteer

from core.web.browser.core.constants.browsers import BrowserNames
from core.web.browser.core.browser.chrome import BrowserChrome
from core.web.browser.core.browser.firefox import BrowserFirefox
from core.web.browser.core.browser.edge import BrowserEdge

TFixture = TypeVar("TFixture")


class WebDriverClass:
    """
    A class that provides a mapping between web driver names and their implementation classes.

    This facilitates the dynamic selection and initialization of web drivers based on
    configuration or runtime choices, supporting different web automation tools like Selenium,
    Playwright, and Puppeteer.
    """

    map = {
        WebDriverNames.SELENIUM.value: DriverSelenium,
        WebDriverNames.PUPPETEER.value: DriverPuppeteer,
        WebDriverNames.PLAYWRIGHT.value: DriverPlaywright,
    }


class BrowserTypeClass:
    """
    A class that maps browser names to their corresponding browser classes.

    This class simplifies the instantiation of browser-specific classes, such as Chrome, Firefox,
    and Edge, allowing for easy expansion to support additional browsers in the future.
    """

    map = {
        BrowserNames.CHROME.value: BrowserChrome,
        BrowserNames.FIREFOX.value: BrowserFirefox,
        BrowserNames.EDGE.value: BrowserEdge,
    }


class BaseFixtureWebDriver(Generic[TWebDriver]):
    """
    A base fixture class for web driver and browser initialization.

    This class takes a web driver configuration and initializes the appropriate web driver
    and browser based on the provided settings. It abstracts away the boilerplate of driver
    setup and provides a unified interface for interacting with the web driver and browser.

    Attributes:
        _config (AppConfigWebDriver): Configuration for the web driver.
        _instance (IWebDriver): The initialized web driver instance.
        _browser (IBrowser): The initialized browser instance.
    """

    def __init__(self, config: AppConfigWebDriver, **kwargs):
        """
        Initializes the web driver and browser based on the provided configuration.

        Args:
            config (AppConfigWebDriver): Configuration for the web driver.
            **kwargs: Additional keyword arguments for driver initialization.
        """
        self._config = config
        self._instance = WebDriverClass.map[config.type](config, **kwargs)
        self._browser = BrowserTypeClass.map[config.browser](self._instance)

        self.kwargs = kwargs
        self.properties = self.get_properties()

    @property
    def loader(self) -> IWebDriver[TWebDriver]:
        """
        Returns the web driver instance.

        Returns:
            IWebDriver[TWebDriver]: The initialized web driver instance.
        """
        return self._instance

    @property
    def driver(self) -> TWebDriver:
        """
        Returns the driver of the web driver instance.

        Returns:
            TWebDriver: The driver attribute of the web driver instance.
        """
        return self._instance.driver

    @property
    def browser(self) -> IBrowser[TBrowser]:
        """
        Returns the browser instance.

        Returns:
            IBrowser[TBrowser]: The initialized browser instance.
        """
        return self._browser

    @property
    def config(self) -> AppConfigWebDriver:
        """
        Returns the configuration.

        Returns:
            Instance of target configuration.
        """
        return self._config

    def get_properties(self) -> dict:
        """
        Returns the web driver fixture properties.
        Returns:
            Key value pairs of the web driver fixture properties.
        """
        props = {}
        for prop_name in dir(self):
            if isinstance(getattr(type(self), prop_name, None), property):
                props[prop_name] = getattr(self, prop_name)
        return props
