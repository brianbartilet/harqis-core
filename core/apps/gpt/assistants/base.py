import time

from typing import Iterable
from core.web.services.manager import WebServiceManager

from core.apps.gpt.contracts.assistant import IAssistant

from core.apps.gpt.services.assistants.assistant import ServiceAssistants
from core.apps.gpt.services.assistants.threads import ServiceThreads
from core.apps.gpt.services.assistants.messages import ServiceMessages
from core.apps.gpt.services.assistants.runs import ServiceRuns

from core.apps.gpt.dto.assistants.assistant import DtoAssistant
from core.apps.gpt.dto.assistants.thread import DtoThread, DtoThreadCreate
from core.apps.gpt.dto.assistants.message import DtoMessage, DtoMessageCreate
from core.apps.gpt.dto.assistants.run import DtoRun, DtoRunCreate

from core.utilities.multiprocess import MultiProcessingClient
from core.utilities.logging.custom_logger import create_logger
from core.utilities.data.qlist import QList

from core.apps.config import AppConfigLoader, AppNames
from http import HTTPStatus


class BaseAssistant(IAssistant):

    def __init__(self, config: AppConfigLoader = None, **kwargs):
        self.log = kwargs.get('logger', create_logger(self.__class__.__name__))
        if config is None:
            self.config = AppConfigLoader(AppNames.API_GPT).config

        self.manager = WebServiceManager(self.config, register=[
            ServiceAssistants,
            ServiceThreads,
            ServiceMessages,
            ServiceRuns
        ])

        super(BaseAssistant, self).__init__(self.config)

        self.kwargs = kwargs

    def load(self, create: bool = True, **kwargs):
        assistant_id = self.config.app_data['default_assistant_id']
        response = self.manager.get(ServiceAssistants).get_assistant(assistant_id)
        self._assistant = response.data

        if response.status_code == HTTPStatus.NOT_FOUND and create:
            payload = DtoAssistant(
                model=self.config.app_data['model'],
                name=f'{self.__class__.__name__}-{self.config.app_data['model']}'
            )
            response_create = self.manager.get(ServiceAssistants).create_assistant(payload)
            self._assistant = response_create.data

    def create_thread(self, thread: DtoThreadCreate = DtoThread()):
        response = self.manager.get(ServiceThreads).create_thread(thread)
        self.threads[f'{response.data.id}'] = response.data

        return response.data

    def add_messages_to_thread(self, messages: Iterable[DtoMessageCreate], thread_id: str = None,
                               create_new=True):

        if create_new:
            self.create_thread()

        thread = next(iter(self.threads.values()))

        use_thread_id = thread_id if thread_id is not None else thread.id
        for message in messages:
            response = self.manager.get(ServiceMessages).create_message(use_thread_id, message)
            self.manager.responses[f'{response.data.id}'] = response.data

    def run_thread(self, thread_id: str = None, run: DtoRunCreate = None):
        use_run = run if run is not None else DtoRunCreate(assistant_id=self._assistant.id)
        thread = next(iter(self.threads.values()))
        use_thread_id = thread_id if thread_id is not None else thread.id

        response = self.manager.get(ServiceRuns).create_run(use_thread_id, use_run)
        self.runs[f'{response.data.id}'] = response.data

    def wait_for_status(self, thread_id: str, run_id: str, wait_secs=1, timeout=60):
        r = self.manager.get(ServiceRuns).get_run(thread_id, run_id)
        time_out = 0
        while r.data.status in ['queued', 'in_progress', 'cancelling']:
            time.sleep(wait_secs)
            r = self.manager.get(ServiceRuns).get_run(thread_id, run_id)
            time_out += 1
            if time_out > timeout:
                self.log.warn(f'Timeout waiting for run {run_id} to complete')

    def wait_for_runs_to_complete(self, multiprocess=False):
        if multiprocess:
            tasks = [(run.thread_id, run.id) for run in self.runs.values()]
            mp_client = MultiProcessingClient(tasks)
            mp_client.execute_tasks(self.wait_for_status, )
        else:
            for run in self.runs.values():
                self.wait_for_status(run.thread_id, run.id)

    def get_messages(self, thread_id: str = None):
        thread = next(iter(self.threads.values()))

        use_thread_id = thread_id if thread_id is not None else thread.id
        response = self.manager.get(ServiceMessages).get_messages(use_thread_id)

        return response.data

    def get_replies(self, thread_id: str = None):
        messages = self.get_messages(thread_id)

        return QList(messages.data).where(lambda x: x.role == 'assistant')

    def prepare_files(self, files: list[str], **kwargs) -> dict:
        pass

    def upload_files(self, files: list[str], **kwargs) -> dict:
        pass

    def download_files(self, files: list[str], **kwargs) -> dict:
        pass

    @property
    def properties(self):
        return self._assistant

