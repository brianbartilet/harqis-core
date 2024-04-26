from typing import Dict, Any, Generic

from core.web.browser.core.contracts.driver import IWebDriver, TWebDriver

from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager

from selenium.webdriver import ChromeOptions, FirefoxOptions, EdgeOptions
from selenium.webdriver import Chrome, Firefox, Edge

from selenium.webdriver.chrome.service import Service as ServiceChrome
from selenium.webdriver.firefox.service import Service as ServiceFirefox
from selenium.webdriver.edge.service import Service as ServiceEdge

from core.web.browser.core.config.web_driver import AppConfigWebDriver
from core.web.browser.core.constants.browsers import BrowserNames


class SeleniumDriverMapping:
    """Maps browser names to their WebDriver manager, options, and driver class.

    Attributes:
        map (Dict[str, Tuple[Any]]): A mapping from browser names to their WebDriver
            manager, options class, and driver class.
    """

    map = {
        BrowserNames.CHROME.value: (ChromeDriverManager, ServiceChrome, ChromeOptions, Chrome),
        BrowserNames.FIREFOX.value: (GeckoDriverManager, ServiceFirefox, FirefoxOptions, Firefox),
        BrowserNames.EDGE.value: (EdgeChromiumDriverManager, ServiceEdge, EdgeOptions, Edge),
    }


class DriverSelenium(IWebDriver[TWebDriver]):
    """A Selenium WebDriver implementation of the IWebDriver interface.

    This class abstracts the creation and management of Selenium WebDriver instances,
    allowing for easy driver and browser configuration through the AppConfigWebDriver object.

    Args:
        config (AppConfigWebDriver): Configuration for the web driver.
        **kwargs: Additional keyword arguments for driver customization.

    Attributes:
        kwargs (Dict[str, Any]): Keyword arguments for driver customization.
        service (Any): The WebDriver manager for the browser.
        options (Any): Configured options for the WebDriver.
        driver (TDriver): The Selenium WebDriver instance.
    """

    def __init__(self, config: AppConfigWebDriver, **kwargs):
        """Initializes a new instance of the DriverSelenium class."""
        super().__init__(config, **kwargs)
        self.kwargs = kwargs
        self._kls_manager = SeleniumDriverMapping.map[self.config.browser][0]
        self._kls_service = SeleniumDriverMapping.map[self.config.browser][1]
        self._kls_options = SeleniumDriverMapping.map[self.config.browser][2]
        self._kls_driver = SeleniumDriverMapping.map[self.config.browser][3]

        self.service = self.get_driver_binary()
        self.options = self.get_driver_options()

        self.driver = self.start()

    def get_driver_options(self) -> Any:
        """Generates options for the Selenium WebDriver based on configuration.

        Returns:
            Any: A configured options instance for the Selenium WebDriver.
        """
        options = self._kls_options()

        if self.config.parameters['headless'] is True:
            options.add_argument("--headless")

        if self.config.options is not None:
            for option in self.config.options:
                options.add_argument(f"{option}")

        return options

    def get_driver_binary(self) -> Any:
        """Retrieves the binary for the WebDriver.

        Returns:
            Any: The path to the installed WebDriver binary.
        """
        service = self._kls_service(self._kls_manager().install())

        return service

    def start(self) -> Generic[TWebDriver]:
        """Starts a new Selenium WebDriver session.

        Returns:
            Any: An instance of the Selenium WebDriver.
        """

        return self._kls_driver(service=self.service, options=self.options)

    def get_info(self) -> Dict[str, Any]:
        """Gets information about the current WebDriver session.

        Returns:
            Dict[str, Any]: A dictionary containing session information.
        """
        raise NotImplementedError

    def get_pid(self) -> int:
        """Gets the process ID of the WebDriver process.

        Returns:
            int: The process ID.
        """
        raise NotImplementedError

    def get_session_id(self) -> str:
        """Gets the session ID of the current WebDriver session.

        Returns:
            str: The session ID.
        """
        raise NotImplementedError

    def close(self) -> None:
        """Closes the current window."""
        raise NotImplementedError

    def quit(self) -> None:
        """Closes the browser and quits the WebDriver session."""
        raise NotImplementedError

