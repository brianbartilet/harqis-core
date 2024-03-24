from abc import abstractmethod, ABC
from typing import Union, TypeVar

# add other inherited interfaces here to extend the functionality
from selenium.webdriver.remote.webelement import WebElement

T = TypeVar("T")
Element = Union[str, WebElement, T]


class IElement(ABC):
    """
    Defines an interface for interacting with web elements within a web page.
    It encapsulates actions like clicking, setting text, and retrieving text.
    """

    @abstractmethod
    def click(self, element: Element) -> None:
        """
        Simulates a mouse click on the specified element.

        Args:
            element: An element locator or a WebElement instance to be clicked.
        """
        ...

    @abstractmethod
    def set_text(self, element: Element, text: str) -> None:
        """
        Enters text into a text input or textarea element.

        Args:
            element: An element locator or a WebElement instance representing the input field.
            text: The text to enter into the input field.
        """
        ...

    @abstractmethod
    def get_text(self, element: Element) -> str:
        """
        Retrieves the visible text from a specified element.

        Args:
            element: An element locator or a WebElement instance to retrieve text from.

        Returns:
            The visible text of the element.
        """
        ...

    @abstractmethod
    def is_visible(self, element: Element) -> bool:
        """
        Checks if the specified element is visible on the page.

        Args:
            element: An element locator or a WebElement instance to check visibility for.

        Returns:
            True if the element is visible, False otherwise.
        """
        ...

    # Additional methods can be defined here.
