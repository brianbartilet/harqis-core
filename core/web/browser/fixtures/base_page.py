from core.web.browser.core.contracts.element import *

from core.web.browser.core.contracts.page import IPage
from core.web.browser.core.contracts.browser import IBrowser
from core.web.browser.core.contracts.driver import IWebDriver


from core.utilities.logging.custom_logger import create_logger
from core.utilities.asserts.helper import LoggedAssertHelper

By = TLocator
WebDriverError = TException
WebElement = TElement
Keys = TKeyboard


class BaseFixturePageObject(IPage):
    """
    Base class for page object models in a web automation framework.
    Provides common functionality for interacting with web pages using dependency injection.

    Attributes:
        driver (TWebDriver): The web driver interface to control the browser.
    """

    def __init__(self, driver: IWebDriver, **kwargs):
        """
        Initialize an instance of the class with a web driver and optional configuration parameters.

        Args:
            driver (IWebDriver): An instance of IWebDriver that facilitates interaction with the web browser.
            **kwargs: Arbitrary keyword arguments that provide additional configuration. Supported keywords include:
                      - logger: An optional logger instance for logging activities. If not provided, a default logger
                                is created based on the class name.
                      - browser: An optional browser interface instance. If not provided, defaults to None.
                      - config: An optional configuration dictionary or object. If not provided, defaults to None.
                      - app_data: An optional dictionary to hold application-specific data.

        Attributes:
            driver (TWebDriver): The web driver instance used for browser interactions.
            log (Logger): The logging instance used to log messages and errors.
            uri (str): The URI of the current page. Used for navigation and verification.
            title (str): The title of the current page.
            _browser (IBrowser, optional): The browser interface instance, to access browser-specific functionalities.
            _config (Any, optional): Configuration data that can be used throughout the instance for various settings.
            _app_data (dict, optional): A dictionary for storing application-specific data
        """
        self.driver = driver

        self.log = kwargs.get('logger', create_logger(self.__class__.__name__))
        self.uri: str = ''
        self.title: str = ''

        self._browser = kwargs.get("browser", None)
        self._config = kwargs.get("config", None)
        self._app_data = kwargs.get("app_data", None)

    def get_page_title(self) -> str:
        """
        Retrieves the title of the current web page.

        Returns:
            str: The title of the page.
        """
        return self.title

    def navigate_to_page(self, url=None) -> None:
        """
        Navigates to a specified URL or to a default URL if none provided.

        Args:
            url (str, optional): The URL to navigate to. If not specified, navigates to the default URL from the config.
        """
        if url is not None:
            self.driver.get(url)
        else:
            self.driver.get(self._config.parameters['url'])

    def login(self, *args) -> None:
        """
        Method to be implemented in subclasses for handling login functionality.

        Raises:
            NotImplementedError: Indicates that the method needs to be implemented in subclasses.
        """
        raise NotImplementedError

    def logout(self, *args) -> None:
        """
        Method to be implemented in subclasses for handling logout functionality.

        Raises:
            NotImplementedError: Indicates that the method needs to be implemented in subclasses.
        """
        raise NotImplementedError

    def wait_page_to_load(self, timeout=30) -> bool:
        """
        Waits for the web page to be loaded completely.
        Override this method in subclasses to add application specific page load conditions.
        Args:
            timeout (int): Maximum time in seconds to wait for the page to load.

        Returns:
            bool: True if the page loads within the timeout, False otherwise.
        """
        return self.driver.wait_page_to_load(timeout)

    def did_page_load(self, *args) -> bool:
        """
        Method to be implemented in subclasses to verify if a page has fully loaded.

        Returns:
            bool: True if the page has loaded completely, otherwise False.

        Raises:
            NotImplementedError: Indicates that the method needs to be implemented in subclasses.
        """
        raise NotImplementedError

    def switch_to_default_content(self) -> None:
        """
        Switches the context to the default content/frame of the web page.
        """
        raise NotImplementedError

    def switch_to_frame(self, frame_reference: str) -> None:
        """
        Switches the context to a specific frame or iframe within the web page.

        Args:
            frame_reference (str): The reference to the frame to switch to, which could be an id, name, or WebElement.
        """
        raise NotImplementedError

    @property
    def browser(self) -> IBrowser:
        """
        Provides access to the browser instance associated with this page object.

        Returns:
            IBrowser: The browser instance.
        """
        return self._browser

    @property
    def config(self) -> IBrowser:
        """
        Provides access to the configuration settings used by this page object.

        Returns:
            IBrowser: The configuration settings.
        """
        return self._config

    @property
    def verify(self) -> LoggedAssertHelper:
        """
        Returns the logged assert helper for performing assertions.

        Return:
            An instance of LoggedAssertHelper.
        """
        return LoggedAssertHelper()

    @property
    def app_data(self) -> dict:
        """
        Returns the application data dictionary.

        Return:
            Application data dictionary.
        """
        return self._app_data
