import unittest

from http import HTTPStatus
from uuid import uuid4

from core.web.services.core.config.webservice import AppConfigWSClient
from core.web.services.manager import WebServiceManager

from core.web.services.tests.rest.service_manager_resources import \
    SimpleTestFixtureResourceOne, SimpleTestFixtureResourceTwo, SimpleTestFixtureResourceThree

test_config = AppConfigWSClient(
    client='rest',
    parameters={
        "base_url": "https://jsonplaceholder.typicode.com/",
        "response_encoding": "utf-8",
        "verify": True
    }
)


class TestWebServiceManager(unittest.TestCase):
    def setUp(self):
        self.mock_config = test_config
        self.manager = WebServiceManager(config=self.mock_config,
                                         register=[SimpleTestFixtureResourceOne, SimpleTestFixtureResourceTwo, ])

    def test_get_service_registered_services(self):
        """Test that get_service correctly initializes a service if not already initialized."""
        service_one = self.manager.get(SimpleTestFixtureResourceOne)
        response_one = service_one.get_request()
        self.assertEqual(response_one.status_code, HTTPStatus.OK)

        service_two = self.manager.get(SimpleTestFixtureResourceTwo)
        response_two = service_two.get_request()
        self.assertEqual(response_two.status_code, HTTPStatus.OK)

    def test_get_service_unregistered(self):
        """Test that get_service incorrectly"""
        service_three = self.manager.get(SimpleTestFixtureResourceThree)
        response_three = service_three.get_request()
        self.assertEqual(response_three.status_code, HTTPStatus.OK)

    def test_get_service_registered(self):
        """Test that get_service incorrectly"""
        self.manager.services.clear()
        self.manager.register(SimpleTestFixtureResourceThree)

        service_three = self.manager.get(SimpleTestFixtureResourceThree)
        response_three = service_three.get_request()
        self.assertEqual(response_three.status_code, HTTPStatus.OK)

    def test_save_and_retrieve_responses(self):
        """Save and retrieve responses from the manager."""
        response_id = f'{uuid4()}'
        service_one = self.manager.get(SimpleTestFixtureResourceOne)
        response_service_one = service_one.get_request()
        self.manager.save_response(response_id, response_service_one)

        response_retrieved = self.manager.get_response(response_id)
        self.assertEqual(response_retrieved.status_code, HTTPStatus.OK)

    def test_save_and_retrieve_multiple_responses(self):
        """Save and retrieve multiple responses from the manager."""
        response_id_one = "one"
        response_id_two = "two"

        service_one = self.manager.get(SimpleTestFixtureResourceOne)
        response_service_one = service_one.get_request()
        self.manager.save_response(response_id_one, response_service_one)

        response_retrieved_one = self.manager.get_response(response_id_one)
        self.assertEqual(response_retrieved_one.status_code, HTTPStatus.OK)

        service_two = self.manager.get(SimpleTestFixtureResourceTwo)
        response_service_two = service_two.get_request()
        self.manager.save_response(response_id_two, response_service_two)

        response_retrieved_two = self.manager.get_response(response_id_two)
        self.assertEqual(response_retrieved_two.status_code, HTTPStatus.OK)

        self.assertEqual(2, len(self.manager.responses))

    def test_get_response_nonexistent(self):
        """Test retrieving a non-existent response returns None."""
        self.assertIsNone(self.manager.get_response("nonexistent"))
