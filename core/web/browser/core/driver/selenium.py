from typing import Dict, Any
import time

from core.web.browser.core.contracts.driver import IWebDriver, TWebDriver

from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager

from selenium.webdriver import ChromeOptions, FirefoxOptions, EdgeOptions
from selenium.webdriver import Chrome, Firefox, Edge

from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.chrome.service import Service as ServiceChrome
from selenium.webdriver.firefox.service import Service as ServiceFirefox
from selenium.webdriver.edge.service import Service as ServiceEdge
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec

from core.web.browser.core.config.web_driver import AppConfigWebDriver
from core.web.browser.core.constants.browsers import BrowserNames


class _DriverTransformClass:
    """A class transformer from configurations

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
        _service (Any): The WebDriver manager for the browser.
        _options (Any): Configured options for the WebDriver.
    """

    def __init__(self, config: AppConfigWebDriver, **kwargs):
        """Initializes a new instance of the DriverSelenium class."""
        super().__init__(config, **kwargs)
        # Retrieve the mapped classes for the specified browser configuration.
        try:
            driver_classes = _DriverTransformClass.map[self.config.browser]
            self._driver_manager, self._driver_service, self._driver_options, self._driver_class = driver_classes
        except KeyError:
            raise ValueError(f"Unsupported browser type {self.config.browser}")

        self._service = self.get_driver_binary()
        self._options = self.get_driver_options()

        self._driver = self.start()

    def get(self, url: str):
        self._driver.get(url)

    def get_driver_options(self) -> Any:
        """Generates options for the Selenium WebDriver based on configuration.

        Returns:
            Any: A configured options instance for the Selenium WebDriver.
        """
        options = self._driver_options()

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
        service = self._driver_service(self._driver_manager().install())

        return service

    def start(self) -> TWebDriver:
        """Starts a new Selenium WebDriver session.

        Returns:
            Any: An instance of the Selenium WebDriver.
        """

        return self._driver_class(service=self._service, options=self._options)

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
        self._driver.close()

    def quit(self) -> None:
        """Closes the browser and quits the WebDriver session."""
        self._driver.quit()

    def find_element(self, locator, value: Any) -> WebElement:
        """
        Finds a single web element using the specified locator and value.

        Args:
            locator (TLocator): The locator strategy, such as By.ID or By.XPATH.
            value (Any): The value of the locator to search for.

        Returns:
            Any: The web element found using the specified locator and value.
        """
        return self._driver.find_element(locator, value)

    def find_elements(self, locator, value: Any) -> list[WebElement]:
        """
        Finds multiple web elements using the specified locator and value.

        Args:
            locator (TLocator): The locator strategy, such as By.ID or By.XPATH.
            value (Any): The value of the locator to search for multiple elements.

        Returns:
            Iterable[Any]: A list of web elements found using the specified locator and value.
        """
        return self._driver.find_elements(locator, value)

    def find_element_by_pattern(self, pattern, locator, value: str) -> Any:
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

    def wait_page_to_load(self, timeout=30, sleep=0.5) -> None:
        """
        Waits for the page to load completely by checking the document's ready state.
        Arguments:
            timeout (int): The maximum time to wait for the page to load, in seconds.
            sleep (float): The time to sleep between checks for the document's ready state.
        """
        time.sleep(sleep)

        def is_page_load_complete(driver):
            """Check if the document's readystate is 'complete'."""
            return self._driver.execute_script("return document.readyState") == "complete"
        try:
            # Wait for the document ready state to be complete.
            WebDriverWait(self._driver, timeout).until(is_page_load_complete)
            # Additional wait for a specific element that signifies the page is fully loaded can be added here.
            # Example: Wait for an element that is known to appear last on the page.
            # WebDriverWait(driver, timeout).until(EC.presence_of_element_located((By.ID, "myElement")))
        except TimeoutError:
            self.log.error("Timed out waiting for page to load")

    def wait_for_element_to_be_visible(self, element, timeout=15, poll_frequency=0.3):
        """
        Waits for the specified element to be visible on the page.
        Args:
            element (Any): The element to wait for.
            timeout (int): The maximum time to wait for the element to be visible.
            poll_frequency (float): The frequency to poll for the element's visibility.
        """
        return WebDriverWait(self._driver, timeout, poll_frequency).until(
            ec.visibility_of(element)) is not None

    def scroll_to_element(self, element: WebElement):
        """Scrolls to the specified element using JavaScript.

        Args:
            element (Any): The web element to scroll to.
        """
        self._driver.execute_script("arguments[0].scrollIntoView();", element)
        self.wait_page_to_load()
        self.log.debug(f"Scrolled to element {element}")

    def high_light_element(self, element: WebElement):
        """Highlights the specified element using JavaScript.

        Args:
            element (Any): The web element to highlight.
        """
        def apply_style(s):
            self._driver.execute_script("arguments[0].setAttribute('style', arguments[1]);", element, s)
            self.log.warn("Potential issue with slow loading - executed script on previous screen.")

        original_style = element.get_attribute('style')
        apply_style("background: yellow; border: 2px solid red;")
        apply_style(original_style)

    def wait_jquery_load(self, time_sec=30):
        """
        Waits for the jquery to complete loading.
        Arguments:
            time_sec (int): The maximum time to wait for jquery to load, in seconds.
        """
        # this is a fix for the error caused by waiting jquery stuff twice.
        # instead of consecutive calls, which appears to mess the driver out
        # we only use one call.
        WebDriverWait(self._driver, time_sec).until(
            lambda d: d.execute_script(
                "return jQuery.active == 0 && $(':animated').length == 0")
        )
        self.log.debug("waiting for animations and for jquery complete")
