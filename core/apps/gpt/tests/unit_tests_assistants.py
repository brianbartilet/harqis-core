import unittest
import time
from uuid import uuid4
from http import HTTPStatus as HttpStatus
from parameterized import parameterized

from core.apps.gpt.services.assistants.assistant import ServiceAssistants
from core.apps.gpt.services.assistants.threads import ServiceThreads
from core.apps.gpt.services.assistants.messages import ServiceMessages
from core.apps.gpt.services.assistants.runs import ServiceRuns

from core.apps.gpt.models.assistants.assistant import Assistant
from core.apps.gpt.models.assistants.thread import Thread, ThreadCreate
from core.apps.gpt.models.assistants.message import Message, MessageCreate
from core.apps.gpt.models.assistants.run import RunCreate

from core.apps.config import AppConfigLoader, AppNames
from core.web.services.core.json import JsonObject

from core.utilities.data.qlist import QList


class TestGPTServicesSmoke(unittest.TestCase):
    """
    Smoke tests for GPT Services.
    """

    def setUp(self):
        """
        Set up the test environment by initializing the GPT service and payload.
        """
        self.given_config = AppConfigLoader(AppNames.API_GPT).config
        self.given_service_assistants = ServiceAssistants(self.given_config)
        self.given_service_threads = ServiceThreads(self.given_config)
        self.given_service_messages = ServiceMessages(self.given_config)
        self.given_service_run = ServiceRuns(self.given_config)

        self.given_payload = Assistant(
            model='gpt-3.5-turbo-0125',
            description='Test assistant',
            name=f'test-assistant-{uuid4()}'
        )
        self.then = self

    def test_assistants_list(self):
        """
        Test the retrieval of the list of assistants.
        """
        when = self.given_service_assistants.get_assistants()
        self.then.assertEqual(when.status_code, HttpStatus.OK)
        self.then.assertIsInstance(when.data, JsonObject)

    def test_assistants_crud_flow(self):
        """
        Test the CRUD (Create, Read, Update, Delete) flow for assistants.
        """
        when = self.given_service_assistants.create_assistant(self.given_payload)
        self.then.assertEqual(when.status_code, HttpStatus.OK)
        self.assertIsInstance(when.data, Assistant)

        assistant_id = when.data.id
        when = self.given_service_assistants.get_assistant(assistant_id)
        self.then.assertEqual(when.status_code, HttpStatus.OK)
        self.then.assertIsInstance(when.data, Assistant)

        given_payload_update = Assistant(description="add a description")
        when = self.given_service_assistants.update_assistant(assistant_id, given_payload_update)
        self.then.assertEqual(when.status_code, HttpStatus.OK)
        self.then.assertIsInstance(when.data, Assistant)
        self.then.assertEqual(when.data.description, given_payload_update.description)

        when = self.given_service_assistants.delete_assistant(assistant_id)
        self.then.assertEqual(when.status_code, HttpStatus.OK)

    @parameterized.expand([
        ('2 + 2', '4'),
        ('2 * 2', '4'),
    ])
    def test_base_assistant_workflow(self, expression, evaluated):
        #  create an assistant
        self.when_create_assistant = self.given_service_assistants.create_assistant(self.given_payload)
        self.then.assertEqual(HttpStatus.OK, self.when_create_assistant.status_code)
        self.assertIsInstance(self.when_create_assistant.data, Assistant)

        #  create a thread
        given_thread_payload = ThreadCreate(messages=[])
        when_create_thread = self.given_service_threads.create_thread(given_thread_payload)
        self.then.assertEqual(HttpStatus.OK, when_create_thread.status_code)
        self.assertIsInstance(when_create_thread.data, Thread)

        #  create a message
        given_thread_id = when_create_thread.data.id
        given_message_payload = MessageCreate(role='user', content='Act as a calculator, digits only')
        when_create_message = self.given_service_messages.create_message(given_thread_id, given_message_payload)
        self.then.assertEqual(HttpStatus.OK, when_create_message.status_code)
        self.assertIsInstance(when_create_message.data, Message)

        #  create a run
        given_run_payload = RunCreate(assistant_id=self.when_create_assistant.data.id,
                                         instructions=f"{expression}")
        when_stream = self.given_service_run.create_run(thread_id=given_thread_id, payload=given_run_payload)
        self.then.assertEqual(HttpStatus.OK, when_stream.status_code)

        #  get the run
        when_get_run = self.given_service_run.get_run(thread_id=given_thread_id,
                                                      run_id=when_stream.data.id)

        self.then.assertEqual(HttpStatus.OK, when_get_run.status_code)

        while when_get_run.data.status in ['queued', 'in_progress', 'cancelling']:
            time.sleep(5)  # Wait for 1 second
            when_get_run = self.given_service_run.get_run(thread_id=given_thread_id,
                                                          run_id=when_stream.data.id)
            self.then.assertEqual(HttpStatus.OK, when_get_run.status_code)

        when_messages = self.given_service_messages.get_messages(thread_id=given_thread_id)
        self.then.assertEqual(HttpStatus.OK, when_messages.status_code)

        target = QList(when_messages.data.data).first()
        content = QList(target.content).first()
        self.then.assertTrue(evaluated in content.text.value)

        #  delete the assistant
        when = self.given_service_assistants.delete_assistant(assistant_id=self.when_create_assistant.data.id)
        self.then.assertEqual(when.status_code, HttpStatus.OK)
