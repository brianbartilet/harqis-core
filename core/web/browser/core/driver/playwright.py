from typing import Dict, Any

from core.web.browser.core.contracts.driver import IWebDriver
from web.browser.core.contracts.driver import TDriver


class DriverPlaywright(IWebDriver):

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

    ...
