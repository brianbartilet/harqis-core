from typing import Dict, Any, Optional, Iterable

from core.web.browser.core.contracts.driver import IWebDriver, TWebDriver


class DriverPlaywright(IWebDriver[TWebDriver]):

    def find_element(self, locator: str, value: Any) -> Optional[Any]:
        raise NotImplementedError

    def find_elements(self, locator: str, value: Any) -> Optional[Iterable[Any]]:
        raise NotImplementedError

    def find_element_by_pattern(self, pattern, locator: str, value: Any) -> Any:
        raise NotImplementedError

    def wait_for_element_to_be_visible(self, *args):
        raise NotImplementedError

    def wait_page_to_load(self, timeout=30):
        raise NotImplementedError

    def scroll_to_element(self, *args):
        raise NotImplementedError

    def high_light_element(self, *args):
        raise NotImplementedError

    def get_driver_options(self) -> Any:
        raise NotImplementedError

    def get_driver_binary(self) -> Any:
        raise NotImplementedError

    def start(self) -> Any:
        raise NotImplementedError

    def get_info(self) -> Dict[str, Any]:
        raise NotImplementedError

    def get_pid(self) -> int:
        raise NotImplementedError

    def get_session_id(self) -> str:
        raise NotImplementedError

    def close(self) -> None:
        raise NotImplementedError

    def quit(self) -> None:
        raise NotImplementedError
