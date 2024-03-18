from apps.gpt.base import BaseServiceHarqisGPT
from apps.gpt.constants.http_headers import HttpHeadersGPT
from apps.gpt.dto.assistants.thread import DtoThread
from apps.gpt.dto.assistants.run import DtoRun

from web.services.core.constants.http_methods import HttpMethod


class ServiceRuns(BaseServiceHarqisGPT):
    """
    Service class for interacting with the OpenAI Assistants API.
    https://platform.openai.com/docs/api-reference/runs
    """
    def __init__(self, config):
        """
        Initializes the ServiceAssistants instance with the given configuration.

        Args:
            config: Configuration object for the service.
        """
        super(ServiceRuns, self).__init__(config)
        self.request\
            .add_header(HttpHeadersGPT.OPEN_API_BETA, "assistants=v1")\
            .add_uri_parameter('threads')

    def create_run(self, thread_id: str, payload: DtoRun):
        """
        Creates a new thread.

        Args:
            thread_id: The ID of the thread.
            payload: Data transfer object containing the thread's configuration.

        Returns:
            The created assistant as a DtoThread object.
        """
        request = self.request\
            .set_method(HttpMethod.POST)\
            .add_uri_parameter(thread_id)\
            .add_json_body(payload) \
            .build()

        return self.client.execute_request(request, response_hook=DtoThread)

