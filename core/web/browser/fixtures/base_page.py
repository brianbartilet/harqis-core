from typing import Iterable, Union, Any

from core.web.browser.core.contracts.page import IPage
from core.web.browser.core.contracts.browser import IBrowser

from core.web.browser.core.contracts.driver import TWebDriver
from core.web.browser.core.contracts.element import TWebElement

from core.utilities.logging.custom_logger import create_logger
from core.utilities.asserts.helper import LoggedAssertHelper

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

TLocator = Union[str, By]


def find_element(locator: TLocator, value: Any) -> Any:
    """
    A decorator that enhances a function to find a single web element using a specified locator and value.

    Args:
        locator (TLocator): The type of locator to use (e.g., By.ID, By.XPATH).
        value (Any): The value associated with the locator.

    Returns:
        Any: A decorator that, when applied, enables the decorated function to locate and return a web element.
    """

    def decorator(func):
        def wrapper(*args):
            try:
                return args[0].driver.find_element(locator, value)
            except Exception as e:
                raise Exception(f"Error {e} finding element with locator: {locator}={value}")

        return wrapper

    return decorator


def find_elements(locator: TLocator, value: str) -> [Any]:
    """
    A decorator that enhances a function to find multiple web elements using a specified locator and value.

    Args:
        locator (TLocator): The type of locator to use (e.g., By.ID, By.XPATH).
        value (str): The value associated with the locator.

    Returns:
        [Any]: A decorator that, when applied, enables the decorated function to locate and return multiple web elements.
    """

    def decorator(func):
        def wrapper(*args) -> []:
            try:
                return args[0].driver.find_elements(locator, value)
            except Exception as e:
                raise Exception(f"Error {e} finding elements with locator: {locator}={value}")

        return wrapper

    return decorator


def find_element_by_pattern(pattern: TWebElement, locator: TLocator, value: str) -> Any:
    """
    A decorator for finding elements based on a specific pattern and locator.

    Args:
        pattern (TWebElement): The pattern of the web element to match.
        locator (TLocator): The type of locator to use (e.g., By.ID, By.XPATH).
        value (str): The value associated with the locator.

    Returns:
        Any: A decorator that, when applied, enables the decorated function to locate and return a web element matching the pattern.
    """

    def decorator(func):
        def wrapper(*args) -> []:
            try:
                return args[0].driver.find_element_by_pattern(pattern, locator, value)
            except Exception as e:
                raise Exception(f"Error {e} finding elements with locator: {locator}={value}")

        return wrapper

    return decorator


class BaseFixturePageObject(IPage):
    """
    Base class for page object models in a web automation framework.
    Provides common functionality for interacting with web pages using dependency injection.

    Attributes:
        driver (TWebDriver): The web driver interface to control the browser.
    """

    def __init__(self, driver: TWebDriver, **kwargs):
        """
        Initialize an instance of the class with a web driver and optional configuration parameters.

        Args:
            driver (TWebDriver): An instance of TWebDriver that facilitates interaction with the web browser.
            **kwargs: Arbitrary keyword arguments that provide additional configuration. Supported keywords include:
                      - logger: An optional logger instance for logging activities. If not provided, a default logger
                                is created based on the class name.
                      - browser: An optional browser interface instance. If not provided, defaults to None.
                      - config: An optional configuration dictionary or object. If not provided, defaults to None.
                      - app_data: An optional dictionary to hold application-specific data. If not provided, defaults to None.

        Attributes:
            driver (TWebDriver): The web driver instance used for browser interactions.
            log (Logger): The logging instance used to log messages and errors.
            _browser (IBrowser, optional): The browser interface instance, may be used to access browser-specific functionalities.
            _config (Any, optional): Configuration data that can be used throughout the instance for various settings.
            _app_data (dict, optional): A dictionary for storing application-specific data that might be needed across different
                                        parts of the application.
        """
        self.driver = driver
        self.log = kwargs.get('logger', create_logger(self.__class__.__name__))

        self._browser = kwargs.get("browser", None)
        self._config = kwargs.get("config", None)
        self._app_data = kwargs.get("app_data", None)

    def get_page_title(self) -> str:
        """
        Retrieves the title of the current web page.

        Returns:
            str: The title of the page.
        """
        return self.driver.title

    def navigate_to_page(self, url=None) -> None:
        """
        Navigates to a specified URL or to a default URL if none provided.

        Args:
            url (str, optional): The URL to navigate to. If not specified, navigates to the default URL from the configuration.
        """
        if url is not None:
            self.driver.get(url)
        else:
            self.driver.get(self._config.parameters['url'])

    def find_element(self, locator: TLocator, value: Any) -> Any:
        """
        Finds a single web element using the specified locator and value.

        Args:
            locator (TLocator): The locator strategy, such as By.ID or By.XPATH.
            value (Any): The value of the locator to search for.

        Returns:
            Any: The web element found using the specified locator and value.
        """
        return self.driver.find_element(locator, value)

    def find_elements(self, locator: TLocator, value: Any) -> Iterable[Any]:
        """
        Finds multiple web elements using the specified locator and value.

        Args:
            locator (TLocator): The locator strategy, such as By.ID or By.XPATH.
            value (Any): The value of the locator to search for multiple elements.

        Returns:
            Iterable[Any]: A list of web elements found using the specified locator and value.
        """
        return self.driver.find_elements(locator, value)

    def find_element_by_pattern(self, pattern: TWebElement, locator: TLocator, value: str) -> Any:
        """
        Method to be implemented in subclasses for finding an element by a specific pattern. Raises NotImplementedError.

        Args:
            pattern (TWebElement): The pattern to match against elements.
            locator (TLocator): The locator strategy, such as By.ID or By.XPATH.
            value (str): The value associated with the locator.

        Returns:
            Any: The element found matching the pattern.

        Raises:
            NotImplementedError: Indicates that the method needs to be implemented in subclasses.
        """
        raise NotImplementedError

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
        def is_page_load_complete(driver):
            """Check if the document's readystate is 'complete'."""
            return driver.execute_script("return document.readyState") == "complete"
        try:
            # Wait for the document ready state to be complete.
            WebDriverWait(self.driver, timeout).until(is_page_load_complete)
            # Additional wait for a specific element that signifies the page is fully loaded can be added here.
            # Example: Wait for an element that is known to appear last on the page.
            # WebDriverWait(driver, timeout).until(EC.presence_of_element_located((By.ID, "myElement")))
            return True
        except TimeoutError:
            self.log.error("Timed out waiting for page to load")
            return False

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
        self.driver.switch_to.default_content()

    def switch_to_frame(self, frame_reference: str) -> None:
        """
        Switches the context to a specific frame or iframe within the web page.

        Args:
            frame_reference (str): The reference to the frame to switch to, which could be an id, name, or WebElement.
        """
        self.driver.switch_to.frame(frame_reference)

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
