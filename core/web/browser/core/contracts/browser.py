from abc import abstractmethod, ABC
from typing import TypeVar, Optional, Dict, Any, Iterable


TDriver = TypeVar("TDriver")
T = TypeVar("T")

class IBrowser(ABC):
    """
    Defines an interface for browser-like behavior, intended as a foundation for
    page object models in web automation or testing. It outlines methods for
    managing browser instances, navigating web pages, and interacting with web elements.
    """

    @abstractmethod
    def get_driver(self) -> TDriver:
        """
        Retrieves the driver instance used by the browser.

        Returns:
            An instance of the driver.
        """
        ...

    @abstractmethod
    def refresh(self) -> None:
        """
        Refreshes the current page in the browser.
        """
        ...

    @abstractmethod
    def close(self) -> None:
        """
        Closes the browser and cleans up any resources.
        """
        ...

    @abstractmethod
    def get(self, url: str) -> None:
        """
        Navigates the browser to the specified URL.

        Args:
            url: The URL to navigate to.
        """
        ...

    @abstractmethod
    def get_session(self) -> T:
        """
        Get session of the browser.
        """
        ...

    @abstractmethod
    def get_cookies(self) -> Iterable[Dict[str, Any]]:
        """
        Get cookies of the browser.
        """
        ...

    @abstractmethod
    def find_element(self, locator: Dict[str, str]) -> Optional[TDriver]:
        """
        Finds a single web element in the current page.

        Args:
            locator: A dictionary defining how to locate the element (e.g., by id, xpath).

        Returns:
            An instance of the element if found, otherwise None.
        """
        ...

    @abstractmethod
    def find_elements(self, locator: Dict[str, str]) -> Optional[TDriver]:
        """
        Finds multiple web elements in the current page.

        Args:
            locator: A dictionary defining how to locate the elements (e.g., by class name, css selector).

        Returns:
            A list of element instances if found, otherwise an empty list.
        """
        ...

    @abstractmethod
    def execute_script(self, script: str, *args) -> Any:
        """
        Executes JavaScript in the context of the currently selected frame or window.

        Args:
            script: The JavaScript code to execute.
            *args: Any arguments required by the JavaScript code.

        Returns:
            The result of the executed script, if any.
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
    def switch_to_default_content(self) -> None:
        """
        Switches the context back to the default document (i.e., out of any iframes).
        """
        ...
