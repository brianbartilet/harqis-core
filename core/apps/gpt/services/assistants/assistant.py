from core.apps.gpt.base_service import BaseServiceHarqisGPT
from core.apps.gpt.constants.http_headers import HttpHeadersGPT
from core.apps.gpt.models.assistants.assistant import Assistant, AssistantFile, ListAssistants
from core.apps.gpt.models.assistants.common import ListQuery, ResponseStatus

from core.web.services.core.json import JsonObject
from core.web.services.core.constants.http_methods import HttpMethod


class ServiceAssistants(BaseServiceHarqisGPT):
    """
    Service class for interacting with the OpenAI Assistants API.
    https://platform.openai.com/docs/api-reference/assistants
    """
    def __init__(self, config):
        """
        Initializes the ServiceAssistants instance with the given configuration.

        Args:
            config: Configuration object for the service.
        """
        super(ServiceAssistants, self).__init__(config)

        self.request\
            .add_header(HttpHeadersGPT.OPEN_API_BETA, "assistants=v2")\
            .set_base_uri('assistants')

    def create_assistant(self, payload: Assistant):
        """
        Creates a new assistant.

        Args:
            payload: Data transfer object containing the assistant's configuration.

        Returns:
            The created assistant as a Assistant object.
        """
        self.request\
            .set_method(HttpMethod.POST)\
            .add_json_body(payload)

        return self.client.execute_request(self.request.build(), response_hook=Assistant)

    def create_assistant_file(self, assistant_id: str, file_id: str):
        """
        Creates a new file for the specified assistant.

        Args:
            assistant_id: The ID of the assistant.
            file_id: file_id of the file to be created.

        Returns:
            The created file as a AssistantFile object.
        """
        self.request \
            .set_method(HttpMethod.POST) \
            .add_uri_parameter(assistant_id)\
            .add_uri_parameter('files') \
            .add_json_body(JsonObject(file_id=file_id)) \

        return self.client.execute_request(self.request.build(), response_hook=AssistantFile)

    def get_assistants(self, query=ListQuery()):
        """
        Retrieves a list of assistants based on the provided query parameters.

        Args:
            query: Data transfer object containing the query parameters.

        Returns:
            A response object containing the list of assistants.
        """
        self.request\
            .set_method(HttpMethod.GET)\
            .add_query_strings(**query.get_dict())

        return self.client.execute_request(self.request.build(), response_hook=ListAssistants)

    def get_assistant_files(self, assistant_id: str, query: ListQuery = None):
        """
        Retrieves a list of files for the specified assistant.

        Args:
            assistant_id: The ID of the assistant.
            query: Data transfer object containing the query parameters (optional).

        Returns:
            A response object containing the list of files.
        """
        self.request \
            .set_method(HttpMethod.POST) \
            .add_uri_parameter(assistant_id)\
            .add_uri_parameter('files') \
            .add_json_body(query)

        return self.client.execute_request(self.request.build(), response_hook=AssistantFile)

    def get_assistant(self, assistant_id: str):
        """
        Retrieves the specified assistant.

        Args:
            assistant_id: The ID of the assistant.

        Returns:
            The retrieved assistant as a Assistant object.
        """

        self.request\
            .set_method(HttpMethod.GET)\
            .add_uri_parameter(assistant_id)

        return self.client.execute_request(self.request.build(), response_hook=Assistant)

    def get_assistant_file(self, assistant_id: str, assistant_file_id: str):
        """
        Retrieves a specific file for the specified assistant.

        Args:
            assistant_id: The ID of the assistant.
            assistant_file_id: The ID of the file.

        Returns:
            The retrieved file as a AssistantFile object.
        """
        self.request\
            .set_method(HttpMethod.GET)\
            .add_uri_parameter(assistant_id)\
            .add_uri_parameter('files')\
            .add_uri_parameter(assistant_file_id)

        return self.client.execute_request(self.request.build(), response_hook=AssistantFile)

    def update_assistant(self, assistant_id: str, payload: Assistant):
        """
        Updates the specified assistant with the given payload.

        Args:
            assistant_id: The ID of the assistant.
            payload: Data transfer object containing the updated configuration.

        Returns:
            The updated assistant as a Assistant object.
        """
        self.request\
            .set_method(HttpMethod.POST)\
            .add_uri_parameter(assistant_id)\
            .add_json_body(payload)\

        return self.client.execute_request(self.request.build(), response_hook=Assistant)

    def delete_assistant(self, assistant_id: str):
        """
        Deletes the specified assistant.

        Args:
            assistant_id: The ID of the assistant.

        Returns:
            A response object indicating the status of the deletion.
        """
        self.request\
            .set_method(HttpMethod.DELETE)\
            .add_uri_parameter(assistant_id)

        return self.client.execute_request(self.request.build(), response_hook=ResponseStatus)

    def delete_assistant_file(self, assistant_id: str, assistant_file_id: str):
        """
        Deletes a specific file for the specified assistant.

        Args:
            assistant_id: The ID of the assistant.
            assistant_file_id: The ID of the file.

        Returns:
            A response object indicating the status of the deletion.
        """
        self.request\
            .set_method(HttpMethod.DELETE)\
            .add_uri_parameter(assistant_id)\
            .add_uri_parameter('files')\
            .add_uri_parameter(assistant_file_id)

        return self.client.execute_request(self.request.build(), response_hook=ResponseStatus)
