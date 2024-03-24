from typing import Any, Iterable

from core.web.browser.core.contracts.page import IPage
from core.web.browser.core.contracts.driver import IWebDriver
from web.browser.core.contracts.page import TElement, TBrowser


def find_element(locator, locator_value: str, suppress_errors=False):
    def decorator(func):
        def wrapper(*args):
            if suppress_errors:
                try:
                    return args[0].driver.find_element(locator, locator_value)
                except Exception as e:
                    return None
            else:
                return args[0].driver.find_element(locator, locator_value)
        return wrapper
    return decorator


def find_elements(locator, locator_value: str):
    def decorator(func):
        def wrapper(*args) -> []:
            return args[0].driver.find_elements(locator, locator_value)
        return wrapper
    return decorator


class BasePage(IPage):

    def __init__(self, driver: IWebDriver, **kwargs):
        self.driver = driver

        self.name = kwargs.get('name', None)
        self.title = kwargs.get('title', None)
        self.id = kwargs.get('id', None)
        self.url = kwargs.get('url', None)

        self.kwargs = kwargs

        #super().__init__(driver)

    def get_browser(self) -> TBrowser:
        pass

    def get_page_title(self) -> str:
        return self.title

    def find_element(self, locator: Any) -> TElement:
        pass

    def find_elements(self, locator: Any) -> Iterable[TElement]:
        pass

    def navigate_to_page(self, *args) -> None:
        pass

    def login(self, *args) -> None:
        pass

    def logout(self, *args) -> None:
        pass

    def wait_page_to_load(self, *args) -> None:
        pass

    def did_page_load(self, *args) -> bool:
        pass

    def switch_to_default_content(self) -> None:
        pass

    def switch_to_frame(self, frame_reference: Any) -> None:
        pass




