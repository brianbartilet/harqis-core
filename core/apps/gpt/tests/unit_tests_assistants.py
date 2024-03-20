import unittest
import time
from uuid import uuid4
from http import HTTPStatus as HttpStatus
from parameterized import parameterized

from apps.gpt.services.assistants.assistant import ServiceAssistants
from apps.gpt.services.assistants.threads import ServiceThreads
from apps.gpt.services.assistants.messages import ServiceMessages
from apps.gpt.services.assistants.runs import ServiceRuns

from apps.gpt.dto.assistants.assistant import DtoAssistant
from apps.gpt.dto.assistants.thread import DtoThread, DtoThreadCreate
from apps.gpt.dto.assistants.message import DtoMessage, DtoMessageCreate
from apps.gpt.dto.assistants.run import DtoRunCreate

from apps.apps_config import AppConfigLoader, AppNames
from web.services.core.json import JsonObject

from utilities.data.qlist import QList


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

        self.given_payload = DtoAssistant(
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
        self.assertIsInstance(when.data, DtoAssistant)

        assistant_id = when.data.id
        when = self.given_service_assistants.get_assistant(assistant_id)
        self.then.assertEqual(when.status_code, HttpStatus.OK)
        self.then.assertIsInstance(when.data, DtoAssistant)

        given_payload_update = DtoAssistant(description="add a description")
        when = self.given_service_assistants.update_assistant(assistant_id, given_payload_update)
        self.then.assertEqual(when.status_code, HttpStatus.OK)
        self.then.assertIsInstance(when.data, DtoAssistant)
        self.then.assertEqual(when.data.description, given_payload_update.description)

        when = self.given_service_assistants.delete_assistant(assistant_id)
        self.then.assertEqual(when.status_code, HttpStatus.OK)

    @parameterized.expand([
        ('2 + 2', '4'),
        ('2 * 2', '4'),
        ('2 / 2', '1'),
        ('2 - 2', '0'),
    ])
    def test_base_assistant_workflow(self, expression, evaluated):
        #  create an assistant
        when_create_assistant = self.given_service_assistants.create_assistant(self.given_payload)
        self.then.assertEqual(HttpStatus.OK, when_create_assistant.status_code)
        self.assertIsInstance(when_create_assistant.data, DtoAssistant)

        #  create a thread
        given_thread_payload = DtoThreadCreate(messages=[])
        when_create_thread = self.given_service_threads.create_thread(given_thread_payload)
        self.then.assertEqual(HttpStatus.OK, when_create_thread.status_code)
        self.assertIsInstance(when_create_thread.data, DtoThread)

        #  create a message
        given_thread_id = when_create_thread.data.id
        given_message_payload = DtoMessageCreate(role='user', content='Hello, world!')
        when_create_message = self.given_service_messages.create_message(given_thread_id, given_message_payload)
        self.then.assertEqual(HttpStatus.OK, when_create_message.status_code)
        self.assertIsInstance(when_create_message.data, DtoMessage)

        #  create a run
        given_run_payload = DtoRunCreate(assistant_id=when_create_assistant.data.id,
                                         instructions=f"Please solve the equation in digits only. What is {expression}")
        when_stream = self.given_service_run.create_run(thread_id=given_thread_id, payload=given_run_payload)
        self.then.assertEqual(HttpStatus.OK, when_stream.status_code)

        #  get the run
        when_get_run = self.given_service_run.get_run(thread_id=given_thread_id,
                                                      run_id=when_stream.data.id)

        self.then.assertEqual(HttpStatus.OK, when_get_run.status_code)

        while when_get_run.data.status in ['queued', 'in_progress', 'cancelling']:
            time.sleep(1)  # Wait for 1 second
            when_get_run = self.given_service_run.get_run(thread_id=given_thread_id,
                                                          run_id=when_stream.data.id)
            self.then.assertEqual(HttpStatus.OK, when_get_run.status_code)

        when_messages = self.given_service_messages.get_messages(thread_id=given_thread_id)
        self.then.assertEqual(HttpStatus.OK, when_messages.status_code)

        target = QList(when_messages.data.data).first()
        content = QList(target.content).first()
        self.then.assertTrue(evaluated in content.text.value)

        #  delete the assistant
        when = self.given_service_assistants.delete_assistant(assistant_id=when_create_assistant.data.id)
        self.then.assertEqual(when.status_code, HttpStatus.OK)