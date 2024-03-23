from abc import ABC, abstractmethod
from typing import TypeVar, Any, Dict

TElement = TypeVar("TElement")


class IWebDriver(ABC):
    """
    Interface for interacting with a web driver, providing essential functionalities to
    control and query the state of the web driver instance. This includes obtaining basic
    driver information, managing sessions, and performing actions on the web browser.
    """

    @abstractmethod
    def get_info(self) -> Dict[str, Any]:
        """
        Retrieves various pieces of information about the web driver instance.

        Returns:
            Dict[str, Any]: A dictionary containing key-value pairs of information about
            the web driver, such as version, capabilities, and other relevant details.
        """
        ...

    @abstractmethod
    def get_pid(self) -> int:
        """
        Obtains the Process ID (PID) of the web driver instance.

        This can be useful for monitoring or managing the web driver process externally.

        Returns:
            int: The PID of the web driver process.
        """
        ...

    @abstractmethod
    def get_session_id(self) -> str:
        """
        Retrieves the session ID of the current web driver session.

        The session ID is a unique identifier for the current session and can be used
        for various purposes, including debugging or session management.

        Returns:
            str: The session ID of the current web driver session.
        """
        ...

    @abstractmethod
    def close(self) -> None:
        """
        Closes the current window, quitting the browser if it's the last window currently open.

        This method should be used when the operations performed in the current window are complete.
        """
        ...

    @abstractmethod
    def quit(self) -> None:
        """
        Quits the web driver session, effectively closing all associated windows and terminating
        the web driver process.

        This method should be called to ensure proper cleanup of resources when the web driver
        is no longer needed.
        """
        ...
