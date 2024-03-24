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
    def get_info(self) -> Dict[str, Any]:
        """
        Retrieves various pieces of information about the browser.

        Returns:
            Dict[str, Any]: A dictionary containing key-value pairs of information about
            the web driver, such as version, capabilities, and other relevant details.
        """
        ...

    @abstractmethod
    def get_version(self) -> str:
        """
        Retrieves various browser version.

        Returns:
            str: Current browser version.
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
    def take_screen_shot(self, *args) -> None:
        """
        Log screenshot of the current page.

        Args:
            *args: Any arguments required by the create screenshot method.

        """
