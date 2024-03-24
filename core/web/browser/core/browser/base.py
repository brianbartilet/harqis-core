from typing import Any, Dict, Iterable

from core.web.browser.core.contracts.browser import IBrowser
from core.web.browser.core.contracts.driver import TDriver


class BaseBrowser(IBrowser):
    """
    Base class for browser implementations. Provides basic browser operations
    by wrapping around a web driver.

    Attributes:
        driver (TDriver): The driver used to interact with the browser.
        kwargs (dict): Additional keyword arguments that can be used for browser customization.

    Methods:
        refresh(): Refreshes the current page.
        close(): Closes the browser.
        get(url: str): Navigates to a specified URL.
        get_session(): Returns the session ID of the current browser session.
        get_cookies(): Returns a list of cookies set in the browser.
        get_info(): Abstract method for retrieving browser information.
        get_version(): Abstract method for retrieving the browser version.
        execute_script(script: str, *args): Executes a JavaScript script on the current page.
    """

    def __init__(self, driver: TDriver, **kwargs):
        """
        Initializes the BaseBrowser with a driver and optional keyword arguments.

        Parameters:
            driver (TDriver): The web driver instance.
            **kwargs: Additional keyword arguments for customization.
        """
        self.driver = driver
        self.kwargs = kwargs

    def refresh(self) -> None:
        """Refreshes the current page."""
        self.driver.refresh()

    def close(self) -> None:
        """Closes the browser window."""
        self.driver.close()

    def get(self, url: str) -> None:
        """Navigates the browser to a specified URL.

        Parameters:
            url (str): The URL to navigate to.
        """
        self.driver.get(url)

    def get_session(self) -> str:
        """Returns the session ID of the current browser session.

        Returns:
            str: The session ID.
        """
        return self.driver.session_id

    def get_cookies(self) -> Iterable[Dict[str, Any]]:
        """Returns a list of cookies set in the browser.

        Returns:
            Iterable[Dict[str, Any]]: A list of dictionaries representing the cookies.
        """
        return self.driver.get_cookies()

    def get_info(self) -> Dict[str, Any]:
        """Abstract method for retrieving browser information.

        Raises:
            NotImplementedError: If the method is not implemented by the subclass.
        """
        raise NotImplementedError

    def get_version(self) -> str:
        """Abstract method for retrieving the browser version.

        Raises:
            NotImplementedError: If the method is not implemented by the subclass.
        """
        raise NotImplementedError

    def execute_script(self, script: str, *args) -> Any:
        """Executes a JavaScript script on the current page.

        Parameters:
            script (str): The JavaScript code to execute.
            *args: Additional arguments to pass to the script.

        Returns:
            Any: The result of the script execution.
        """
        return self.driver.execute_script(script, *args)
