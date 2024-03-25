from typing import Any, Dict, Iterable

from core.web.browser.core.contracts.browser import IBrowser


class BrowserChrome(IBrowser):
    """
    Represents a Chrome browser instance for web automation.

    This class extends BaseBrowser, providing specific implementations and
    configurations necessary for controlling and interacting with the Chrome browser.
    It utilizes the functionalities defined in BaseBrowser and may add Chrome-specific
    features or overrides as required for Chrome automation tasks.

    Attributes:
        Inherits all attributes from the BaseBrowser class.
    """

    def refresh(self) -> None:
        self.driver.refresh()

    def close(self) -> None:
        self.driver.close()

    def get(self, url: str) -> None:
        self.driver.get(url)

    def get_session(self) -> str:
        return self.driver.session_id

    def get_cookies(self) -> Iterable[Dict[str, Any]]:
        return self.driver.get_cookies()

    def get_info(self) -> Dict[str, Any]:
        return self.driver.get_info()

    def get_version(self) -> str:
        raise NotImplementedError

    def execute_script(self, script: str, *args) -> Any:
        self.driver.execute_script(script, *args)

    def take_screen_shot(self, *args) -> None:
        raise NotImplementedError


