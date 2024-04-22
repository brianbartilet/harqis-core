from abc import ABC, abstractmethod
from typing import Any, Dict, Iterable

from core.web.services.core.config.webservice import AppConfigWSClient
from core.web.services.manager import WebServiceManager

from core.apps.gpt.models.assistants.thread import Thread


class IAssistant(ABC):
    """
    Abstract base class for managing threads, messages, and files in an assistant-like interface.

    Attributes:
        config (AppConfigWSClient): Configuration object for web service client.
        threads (Dict[str, Thread]): Dictionary to store thread instances by their identifiers.
        runs (Dict[str, Any]): Dictionary to store run-specific data.
        messages (Dict[str, Any]): Dictionary to store messages.
        files (Dict[str, Any]): Dictionary to store file data.
        manager (WebServiceManager): Manager to handle web service operations.
        _assistant: Internal variable to store assistant-specific state or objects.
    """

    def __init__(self, config: AppConfigWSClient, **kwargs):
        """
        Initializes the IAssistant with a given configuration.

        Args:
            config (AppConfigWSClient): Configuration for the assistant's web service client.
            **kwargs: Arbitrary keyword arguments that may be used for extending initialization.
        """
        self.config = config
        self.kwargs = kwargs

        self.threads: Dict[str, Thread] = {}
        self.runs: Dict[str, Any] = {}
        self.messages: Dict[str, Any] = {}
        self.files: Dict[str, Any] = {}

        self.manager: WebServiceManager

        self._assistant = None

    @abstractmethod
    def load(self, **kwargs):
        """
        Loads necessary data or states needed by the assistant.

        Args:
            **kwargs: Arbitrary keyword arguments for loading specific configurations or states.
        """
        ...

    @abstractmethod
    def create_thread(self, **kwargs) -> Any:
        """
        Creates and returns a new thread based on given parameters.

        Args:
            **kwargs: Arbitrary keyword arguments needed for creating a thread.

        Returns:
            Any: A new thread instance.
        """
        ...

    @abstractmethod
    def add_messages_to_thread(self, **kwargs):
        """
        Adds messages to a specific thread identified by arguments.

        Args:
            **kwargs: Arbitrary keyword arguments containing thread identifiers and message details.
        """
        ...

    @abstractmethod
    def run_thread(self, **kwargs):
        """
        Executes operations within a specified thread.

        Args:
            **kwargs: Arbitrary keyword arguments identifying the thread and execution details.
        """
        ...

    @abstractmethod
    def wait_for_runs_to_complete(self, **kwargs):
        """
        Waits for all initiated runs to complete.

        Args:
            **kwargs: Arbitrary keyword arguments specifying which runs to wait for.
        """
        ...

    @abstractmethod
    def get_messages(self, **kwargs):
        """
        Retrieves messages based on specified criteria.

        Args:
            **kwargs: Arbitrary keyword arguments detailing the retrieval criteria.

        Returns:
            Dict[str, Any]: A dictionary containing the requested messages.
        """
        ...

    @abstractmethod
    def get_replies(self, **kwargs):
        """
        Retrieves replies for messages based on specified criteria.

        Args:
            **kwargs: Arbitrary keyword arguments detailing the retrieval criteria.
        """
        ...

    @abstractmethod
    def prepare_files(self, *args, **kwargs) -> dict:
        """
        Prepares file data for uploading or processing.

        Args:
            *args: Arbitrary positional arguments.
            **kwargs: Arbitrary keyword arguments related to file preparation.

        Returns:
            dict: Dictionary containing prepared file data.
        """
        ...

    @abstractmethod
    def upload_files(self, *args, **kwargs) -> Iterable[Any]:
        """
        Uploads files based on provided data.

        Args:
            *args: Arbitrary positional arguments.
            **kwargs: Arbitrary keyword arguments related to file uploading.

        Returns:
            Iterable[Any]: An iterable of upload results or identifiers.
        """
        ...

    @abstractmethod
    def download_file(self, *args, **kwargs) -> dict:
        """
        Downloads a single file based on specified criteria.

        Args:
            *args: Arbitrary positional arguments.
            **kwargs: Arbitrary keyword arguments for file download.

        Returns:
            dict: Dictionary containing the downloaded file data.
        """
        ...

    @abstractmethod
    def download_files(self, *args, **kwargs) -> dict:
        """
        Downloads multiple files based on specified criteria.

        Args:
            *args: Arbitrary positional arguments.
            **kwargs: Arbitrary keyword arguments for multiple file downloads.

        Returns:
            dict: Dictionary containing the downloaded files data.
        """
        ...

    @abstractmethod
    def wait_for_run_to_complete(self, **kwargs):
        """
        Waits for a specific run to complete based on given criteria.

        Args:
            **kwargs: Arbitrary keyword arguments specifying the run to wait for.
        """
        ...
