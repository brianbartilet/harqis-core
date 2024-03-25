from typing import Dict, Any

from core.web.browser.core.contracts.driver import IWebDriver, TWebDriver


class DriverPlaywright(IWebDriver[TWebDriver]):

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

