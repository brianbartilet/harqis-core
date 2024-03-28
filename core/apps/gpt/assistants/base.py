import time

from typing import Iterable
from core.web.services.manager import WebServiceManager

from core.apps.gpt.contracts.assistant import IAssistant

from core.apps.gpt.constants.status import RunStatus

from core.apps.gpt.services.assistants.assistant import ServiceAssistants
from core.apps.gpt.services.assistants.threads import ServiceThreads
from core.apps.gpt.services.assistants.messages import ServiceMessages
from core.apps.gpt.services.assistants.runs import ServiceRuns
from core.apps.gpt.services.files import ServiceFiles

from core.apps.gpt.models.assistants.assistant import Assistant
from core.apps.gpt.models.assistants.thread import Thread, ThreadCreate
from core.apps.gpt.models.assistants.message import Message, MessageCreate
from core.apps.gpt.models.assistants.run import Run, RunCreate

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
            ServiceRuns,
            ServiceFiles,
        ])

        super(BaseAssistant, self).__init__(self.config)

        self.kwargs = kwargs

    def load(self, create: bool = True, **kwargs):
        assistant_id = self.config.app_data['default_assistant_id']
        response = self.manager.get(ServiceAssistants).get_assistant(assistant_id)
        self._assistant = response.data

        if response.status_code == HTTPStatus.NOT_FOUND and create:
            payload = Assistant(
                model=self.config.app_data['model'],
                name=f'{self.__class__.__name__}-{self.config.app_data['model']}'
            )
            response_create = self.manager.get(ServiceAssistants).create_assistant(payload)
            self._assistant = response_create.data

    def create_thread(self, thread: ThreadCreate = Thread()):
        response = self.manager.get(ServiceThreads).create_thread(thread)
        self.threads[f'{response.data.id}'] = response.data

        return response.data

    def add_messages_to_thread(self, messages: Iterable[MessageCreate], thread_id: str = None,
                               create_new=True):

        if create_new:
            self.create_thread()

        thread = next(iter(self.threads.values()))

        use_thread_id = thread_id if thread_id is not None else thread.id
        for message in messages:
            response = self.manager.get(ServiceMessages).create_message(use_thread_id, message)
            self.manager.responses[f'{response.data.id}'] = response.data

    def run_thread(self, thread_id: str = None, run: RunCreate = None):
        use_run = run if run is not None else RunCreate(assistant_id=self._assistant.id)
        thread = next(iter(self.threads.values()))
        use_thread_id = thread_id if thread_id is not None else thread.id

        response = self.manager.get(ServiceRuns).create_run(use_thread_id, use_run)
        self.runs[f'{response.data.id}'] = response.data

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

    def upload_files(self, base_directory: str, file_patterns: list = None, **kwargs):
        file_patterns = file_patterns if file_patterns is not None else ['*.py', '*.json', '*.yaml']

        files = self.manager.get(ServiceFiles).upload_files(file_names=[], base_path=base_directory)
        self.files = {file.id: file for file in files}
        return files

    def download_files(self, files: list[str], **kwargs) -> dict:
        pass

    def wait_for_status(self, thread_id: str, run_id: str, wait_secs=1, retries=60 * 2):
        r = self.manager.get(ServiceRuns).get_run(thread_id, run_id)
        time_out = 0
        while r.data.status in [RunStatus.QUEUED.value, RunStatus.IN_PROGRESS.value, RunStatus.CANCELLING.value]:
            time.sleep(wait_secs)
            r = self.manager.get(ServiceRuns).get_run(thread_id, run_id)
            time_out += 1
            if time_out > retries:
                self.log.warn(f'Timeout waiting for run {run_id} to complete')

    @property
    def properties(self):
        return self._assistant

