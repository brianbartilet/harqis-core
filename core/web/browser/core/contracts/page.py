from abc import ABC, abstractmethod
from typing import TypeVar, Any, Iterable

TBrowser = TypeVar("TBrowser")
TElement = TypeVar("TElement")


class IPage(ABC):
    """
    Defines the interface for a generic page object model.

    This interface encapsulates the behavior expected from a web page in a web automation
    framework, including navigation, element interaction, and condition checks for page load.
    """

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
    def get_browser(self) -> TBrowser:
        """
        Retrieves the browser instance associated with this page.

        Returns:
            TBrowser: An instance of the browser used to navigate the page.
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
    def find_element(self, locator: Any) -> TElement:
        """
        Finds an element on the page.

        Args:
            locator: The strategy and locator of the element to find.

        Returns:
            TElement: An instance of the found element.
        """
        ...

    @abstractmethod
    def find_elements(self, locator: Any) -> Iterable[TElement]:
        """
        Finds a collection of elements on the page matching the given locator.

        Args:
            locator: The strategy and locator of the elements to find.

        Returns:
            Iterable[TElement]: A collection of instances of the found elements.
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
    def wait_page_to_load(self, *args) -> None:
        """
        Waits for the page to load until certain conditions are met.

        Args:
            *args: Optional conditions to wait for.
        """
        ...
