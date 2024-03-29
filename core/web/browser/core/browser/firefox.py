from typing import Any, Dict, Iterable

from core.web.browser.core.contracts.browser import IBrowser


class BrowserFirefox(IBrowser):
    """
    Represents a Mozilla Firefox browser instance for web automation.

    This class extends BaseBrowser, providing specific implementations and
    configurations necessary for controlling and interacting with the Firefox browser.
    It utilizes the functionalities defined in BaseBrowser and may add Firefox-specific
    features or overrides as required for Firefox automation tasks.

    Attributes:
        Inherits all attributes from the BaseBrowser class.
    """

    def refresh(self) -> None:
        raise NotImplementedError

    def close(self) -> None:
        raise NotImplementedError

    def get_session(self) -> Any:
        raise NotImplementedError

    def get_cookies(self) -> Iterable[Dict[str, Any]]:
        raise NotImplementedError

    def get_info(self) -> Dict[str, Any]:
        raise NotImplementedError

    def get_version(self) -> str:
        raise NotImplementedError

    def execute_script(self, script: str, *args) -> Any:
        raise NotImplementedError

    def take_screen_shot(self, *args) -> None:
        raise NotImplementedError


