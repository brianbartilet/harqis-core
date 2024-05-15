from abc import ABC, abstractmethod
from abc import ABC, abstractmethod
from typing import TypeVar, Any, Dict, Union, Generic, Optional, Iterable

from core.utilities.logging.custom_logger import create_logger
from core.web.browser.core.contracts.element import TElement

# add other inherited interfaces here to extend the functionality
from selenium.webdriver.remote.webdriver import WebDriver

T = TypeVar("T", bound=WebDriver)
TWebDriver = Union[T, ]


class IWebDriver(ABC, Generic[TWebDriver]):
    """
    Interface for interacting with a web driver, providing essential functionalities to
    control and query the state of the web driver instance. This includes obtaining basic
    driver information, managing sessions, and performing actions on the web browser.
    """

    def __init__(self, config, **kwargs):
        self.config = config
        self.log = kwargs.get('logger', create_logger(self.__class__.__name__))
        self._driver = None

    # region Abstract Methods For Driver Implementation

    @abstractmethod
    def get_driver_options(self) -> Any:
        """
        Retrieves the driver options for the web driver instance.

        Returns:
            Any: The driver options object for the web driver.
        """
        ...

    @abstractmethod
    def get_driver_binary(self) -> Any:
        """
        Retrieves the driver executable binary for the web driver instance.
        Returns:
            Any: The driver executable binary for the web driver.
        """
        ...

    @abstractmethod
    def get_info(self) -> Dict[str, Any]:
        """
        Retrieves various pieces of information about the web driver instance.

        Returns:
            Dict[str, Any]: A dictionary containing key-value pairs of information about
            the web driver, such as version, capabilities, and other relevant details.
        """
        ...

    @abstractmethod
    def get_pid(self) -> int:
        """
        Obtains the Process ID (PID) of the web driver instance.

        This can be useful for monitoring or managing the web driver process externally.

        Returns:
            int: The PID of the web driver process.
        """
        ...

    @abstractmethod
    def get_session_id(self) -> str:
        """
        Retrieves the session ID of the current web driver session.

        The session ID is a unique identifier for the current session and can be used
        for various purposes, including debugging or session management.

        Returns:
            str: The session ID of the current web driver session.
        """
        ...

    @abstractmethod
    def start(self) -> TWebDriver:
        """
        starts the web driver session, initializing the web driver instance and opening a new window.

        Returns:
            Any: The web driver instance that was started.
        """
        ...

    @abstractmethod
    def get(self, *args) -> None:
        """
        navigate to base url
        """
        ...

    @abstractmethod
    def close(self) -> None:
        """
        Closes the current window, quitting the browser if it's the last window currently open.

        This method should be used when the operations performed in the current window are complete.
        """
        ...

    @abstractmethod
    def quit(self) -> None:
        """
        Quits the web driver session, effectively closing all associated windows and terminating
        the web driver process.

        This method should be called to ensure proper cleanup of resources when the web driver
        is no longer needed.
        """
        ...
    # endregion

    # region Abstract Methods For Driver Actions

    @abstractmethod
    def find_element(self, locator: str, value: Any) -> TElement:
        """
        Finds a single web element in the current page.

        Args:
            locator: locator type (e.g., by id, xpath).
            value: value of the locator.

        Returns:
            An instance of the element if found, otherwise None.
        """
        ...

    @abstractmethod
    def find_elements(self, locator: str, value: Any) -> list[TElement]:
        """
        Finds multiple web elements in the current page.

        Args:
            locator: locator type (e.g., by id, xpath).
            value: value of the locator.

        Returns:
            A list of element instances if found, otherwise an empty list.
        """
        ...

    @abstractmethod
    def find_element_by_pattern(self, pattern, locator: str, value: Any) -> Any:
        """
        Finds a web element using a pattern in the current page.

        Args:
            pattern: The pattern to use for finding the element.
            locator: The locator type (e.g., by id, xpath).
            value: The value of the locator.

        Returns:
            The element instance if found, otherwise None.
        """
        ...

    @abstractmethod
    def wait_for_element_to_be_visible(self,  *args, **kwargs):
        """
        Waits for the specified element to be visible on the page.
        """
        ...

    @abstractmethod
    def wait_page_to_load(self, *args, **kwargs):
        """
        Waits for the page to load, with an optional timeout.
        """
        ...

    @abstractmethod
    def scroll_to_element(self,  *args, **kwargs):
        """Scrolls to the specified element using JavaScript.
        """
        ...

    @abstractmethod
    def high_light_element(self,   *args, **kwargs):
        """Highlights the specified element using JavaScript.
        """
        ...

    # endregion
