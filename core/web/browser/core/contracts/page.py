from abc import abstractmethod, ABC
from typing import Any


class IPage(ABC):

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
    def wait_page_to_load(self, *args) -> Any:
        """
        Waits for the page to load until certain conditions are met.

        Args:
            *args: Optional conditions to wait for.
        """
        ...
