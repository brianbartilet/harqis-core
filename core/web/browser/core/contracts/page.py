from abc import abstractmethod, ABC
from typing import Optional, Dict, Any, Iterable

from core.web.browser.core.contracts.driver import TDriver, IWebDriver

from core.web.browser.core.contracts.element import TWebElement


class IPage(ABC):
    """
    Defines the interface for a generic page object model.

    This interface encapsulates the behavior expected from a web page in a web automation
    framework, including navigation, element interaction, and condition checks for page load.
    """
    def __init__(self, driver: TDriver, **kwargs):
        self.driver = driver

        self._browser = None
        self._config = None
        self._app_data = kwargs.get("app_data", None)

        self.kwargs = kwargs

    @abstractmethod
    def did_page_load(self, *args) -> bool:
        """
        Checks if the page has loaded successfully.

        Args:
            *args: Optional arguments to determine specific load conditions.

        Returns:
            bool: True if the page is considered loaded, False otherwise.
        """
        ...

    @abstractmethod
    def get_page_title(self) -> str:
        """
        Retrieves the title of the current page.

        Returns:
            str: The title of the page.
        """
        ...

    @abstractmethod
    def find_element(self, locator: str, value: Any) -> Optional[Any]:
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
    def find_elements(self, locator: str, value: Any) -> Optional[Iterable[Any]]:
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
    def find_element_by_pattern(self, pattern: TWebElement, locator: str, value: Any) -> Any:
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
    def navigate_to_page(self, *args) -> None:
        """
        Navigates the browser to the page represented by this page object.

        Args:
            *args: Optional arguments specifying the navigation details.
        """
        ...

    @abstractmethod
    def login(self, *args) -> None:
        """
        Performs login operation if applicable for the page.

        Args:
            *args: Credentials and any additional login parameters.
        """
        ...

    @abstractmethod
    def logout(self, *args) -> None:
        """
        Performs logout operation if applicable for the page.

        Args:
            *args: Any parameters needed for the logout operation.
        """
        ...

    @abstractmethod
    def switch_to_default_content(self) -> None:
        """
        Switches the context back to the default document (i.e., out of any iframes).
        """
        ...

    @abstractmethod
    def switch_to_frame(self, frame_reference: Any) -> None:
        """
        Switches the context to the specified frame.

        Args:
            frame_reference: The reference to the frame to switch to (e.g., an index, name, or element).
        """
        ...

    @abstractmethod
    def wait_page_to_load(self, *args) -> None:
        """
        Waits for the page to load until certain conditions are met.

        Args:
            *args: Optional conditions to wait for.
        """
        ...
