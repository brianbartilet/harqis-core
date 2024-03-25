from abc import ABC
from typing import Union, TypeVar, Generic

from core.web.browser.core.contracts.driver import IWebDriver

# add other inherited interfaces here to extend the functionality
from selenium.webdriver.remote.webelement import WebElement

T = TypeVar("T", bound=WebElement)
TWebElement = Union[T,]


class IWebElement(ABC, Generic[TWebElement]):
    """
    Defines an interface for interacting with web elements within a web page.
    It encapsulates actions like clicking, setting text, and retrieving text.
    """

    def __init__(self, driver: IWebDriver, element_template=None, **kwargs):
        """
        Initializes the BaseElement with a driver and optional keyword arguments.

        Parameters:
            driver (IWebDriver): The web driver instance.
            element_template (TElement): The element template to use for locating elements.
            **kwargs: Additional keyword arguments for customization.
        """
        self.driver = driver
        self.element_template = element_template
        self.kwargs = kwargs
