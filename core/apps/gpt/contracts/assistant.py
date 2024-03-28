from abc import ABC, abstractmethod
from typing import Any, Dict, Iterable

from core.web.services.core.config.webservice import AppConfigWSClient
from core.web.services.manager import WebServiceManager

from core.apps.gpt.models.assistants.thread import Thread


class IAssistant(ABC):
    def __init__(self, config: AppConfigWSClient, **kwargs):
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
        ...

    @abstractmethod
    def create_thread(self, **kwargs) -> Any:
        ...

    @abstractmethod
    def add_messages_to_thread(self, **kwargs):
        ...

    @abstractmethod
    def run_thread(self, **kwargs):
        ...

    @abstractmethod
    def wait_for_runs_to_complete(self, **kwargs):
        ...

    @abstractmethod
    def get_messages(self, **kwargs):
        ...

    @abstractmethod
    def get_replies(self, **kwargs):
        ...

    @abstractmethod
    def prepare_files(self, *args, **kwargs) -> dict:
        ...

    @abstractmethod
    def upload_files(self, *args, **kwargs) -> Iterable[Any]:
        ...

    @abstractmethod
    def download_files(self, *args, **kwargs) -> dict:
        ...

    @abstractmethod
    def wait_for_status(self, **kwargs):
        ...
