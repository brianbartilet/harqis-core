import unittest
from http import HTTPStatus as HttpStatus

from apps.gpt.services.assistants.assistant import ServiceAssistants
from apps.gpt.services.assistants.threads import ServiceThreads
from apps.gpt.dto.assistants.assistant import DtoAssistant
from apps.gpt.dto.assistants.thread import DtoThread

from apps.apps_config import AppConfigLoader, AppNames
from uuid import uuid4
from web.services.core.json import JsonObject


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

    def test_base_assistant_workflow(self):
        when_create_assistant = self.given_service_assistants.create_assistant(self.given_payload)
        self.then.assertEqual(when_create_assistant.status_code, HttpStatus.OK)
        self.assertIsInstance(when_create_assistant.data, DtoAssistant)

        given_thread_payload = DtoThread(
            assistant_id=when_create_assistant.data.id,
            name=f'test-thread-{uuid4()}'
        )
        when_create_thread = self.given_service_threads.create_thread(given_thread_payload)
        self.then.assertEqual(when_create_thread.status_code, HttpStatus.CREATED)
        self.assertIsInstance(when_create_thread.data, DtoThread)
