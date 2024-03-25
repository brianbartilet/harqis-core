from typing import Iterable, Union, Any

from core.web.browser.core.contracts.page import IPage
from core.web.browser.core.contracts.browser import IBrowser

from core.web.browser.core.contracts.driver import TDriver
from core.web.browser.core.contracts.element import TWebElement

from core.utilities.asserts.helper import LoggedAssertHelper

from selenium.webdriver.common.by import By
TLocator = Union[str, By]


def find_element(locator: TLocator, value: Any) -> Any:
    def decorator(func):
        def wrapper(*args):
            try:
                return args[0].driver.find_element(locator, value)
            except Exception as e:
                raise Exception(f"Error {e} finding element with locator: {locator}={value}")
        return wrapper
    return decorator


def find_elements(locator: TLocator, value: str) -> [Any]:
    def decorator(func):
        def wrapper(*args) -> []:
            try:
                return args[0].driver.find_elements(locator, value)
            except Exception as e:
                raise Exception(f"Error {e} finding elements with locator: {locator}={value}")
        return wrapper
    return decorator


def find_element_by_pattern(self, pattern: TWebElement, locator: TLocator, value: str) -> Any:
    def decorator(func):
        def wrapper(*args) -> []:
            try:
                return args[0].driver.find_element_by_pattern(pattern, locator, value)
            except Exception as e:
                raise Exception(f"Error {e} finding elements with locator: {locator}={value}")

        return wrapper

    return decorator


class BasePageObjectModel(IPage):

    def __init__(self, driver: TDriver, **kwargs):
        super().__init__(driver, **kwargs)

        self._browser = None
        self._config = None

    def get_page_title(self) -> str:
        return self.driver.session_id

    def find_element(self, locator: TLocator, value: Any) -> Any:
        return self.driver.find_element(locator, value)

    def find_elements(self, locator: TLocator, value: Any) -> Iterable[Any]:
        return self.driver.find_elements(locator, value)

    def find_element_by_pattern(self, pattern: TWebElement, locator: TLocator, value: str) -> Any:
        raise NotImplementedError

    def navigate_to_page(self, url) -> None:
        self.driver.get(url)

    def login(self, *args) -> None:
        raise NotImplementedError

    def logout(self, *args) -> None:
        raise NotImplementedError

    def wait_page_to_load(self, *args) -> None:
        raise NotImplementedError

    def did_page_load(self, *args) -> bool:
        raise NotImplementedError

    def switch_to_default_content(self) -> None:
        self.driver.switch_to.default_content()

    def switch_to_frame(self, frame_reference: str) -> None:
        self.driver.switch_to.frame(frame_reference)

    @property
    def browser(self) -> IBrowser:
        return self._browser

    @property
    def config(self) -> IBrowser:
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
