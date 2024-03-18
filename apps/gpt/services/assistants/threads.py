from apps.gpt.base import BaseServiceHarqisGPT
from apps.gpt.constants.http_headers import HttpHeadersGPT
from apps.gpt.dto.assistants.thread import DtoThread
from apps.gpt.dto.assistants.common import DtoResponseStatus

from web.services.core.constants.http_methods import HttpMethod


class ServiceThreads(BaseServiceHarqisGPT):
    """
    Service class for interacting with the OpenAI Assistants API.
    https://platform.openai.com/docs/api-reference/threads
    """
    def __init__(self, config):
        """
        Initializes the ServiceAssistants instance with the given configuration.

        Args:
            config: Configuration object for the service.
        """
        super(ServiceThreads, self).__init__(config)
        self.request\
            .add_header(HttpHeadersGPT.OPEN_API_BETA, "assistants=v1")\
            .add_uri_parameter('threads')

    def create_thread(self, payload: DtoThread):
        """
        Creates a new thread.

        Args:
            payload: Data transfer object containing the thread's configuration.

        Returns:
            The created assistant as a DtoThread object.
        """
        request = self.request\
            .set_method(HttpMethod.POST)\
            .add_json_body(payload) \
            .build()

        return self.client.execute_request(request, response_hook=DtoThread)

    def get_thread(self, thread_id: str):
        """
        Get thread object by ID.

        Args:
            thread_id: Data transfer object containing the thread's configuration.

        Returns:
            The thread object
        """
        request = self.request\
            .set_method(HttpMethod.GET)\
            .add_uri_parameter(thread_id) \
            .build()

        return self.client.execute_request(request, response_hook=DtoThread)

    def update_thread(self, thread_id: str, payload: DtoThread):
        """
        Get thread object by ID.

        Args:
            thread_id: Data transfer object containing the thread's configuration.
            payload: Data transfer object containing the thread's configuration.

        Returns:
            The thread object
        """
        request = self.request\
            .set_method(HttpMethod.POST)\
            .add_uri_parameter(thread_id) \
            .add_json_body(payload) \
            .build()

        return self.client.execute_request(request, response_hook=DtoThread)

    def delete_thread(self, thread_id: str):
        """
        Delete thread object by ID.

        Args:
            thread_id: Data transfer object containing the thread's configuration.

        Returns:
            The thread object
        """
        request = self.request\
            .set_method(HttpMethod.DELETE)\
            .add_uri_parameter(thread_id) \
            .build()

        return self.client.execute_request(request, response_hook=DtoResponseStatus)

