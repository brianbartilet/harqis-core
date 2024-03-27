from core.apps.gpt.base_service import BaseServiceHarqisGPT
from core.apps.gpt.constants.http_headers import HttpHeadersGPT
from core.apps.gpt.dto.assistants.assistant import DtoAssistant, DtoAssistantFile, DtoListAssistants
from core.apps.gpt.dto.assistants.common import DtoListQuery, DtoResponseStatus

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
            .add_header(HttpHeadersGPT.OPEN_API_BETA, "assistants=v1")\
            .add_uri_parameter('assistants')

    def create_assistant(self, payload: DtoAssistant):
        """
        Creates a new assistant.

        Args:
            payload: Data transfer object containing the assistant's configuration.

        Returns:
            The created assistant as a DtoAssistant object.
        """
        self.request\
            .set_method(HttpMethod.POST)\
            .add_json_body(payload)

        return self.client.execute_request(self.request.build(), response_hook=DtoAssistant)

    def create_assistant_file(self, assistant_id: str, file_id: str):
        """
        Creates a new file for the specified assistant.

        Args:
            assistant_id: The ID of the assistant.
            file_id: file_id of the file to be created.

        Returns:
            The created file as a DtoAssistantFile object.
        """
        self.request \
            .set_method(HttpMethod.POST) \
            .add_uri_parameter(assistant_id)\
            .add_uri_parameter('files') \
            .add_json_body(JsonObject(file_id=file_id)) \

        return self.client.execute_request(self.request.build(), response_hook=DtoAssistantFile)

    def get_assistants(self, query=DtoListQuery()):
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

        return self.client.execute_request(self.request.build(), response_hook=DtoListAssistants)

    def get_assistant_files(self, assistant_id: str, query: DtoListQuery = None):
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

        return self.client.execute_request(self.request.build(), response_hook=DtoAssistantFile)

    def get_assistant(self, assistant_id: str):
        """
        Retrieves the specified assistant.

        Args:
            assistant_id: The ID of the assistant.

        Returns:
            The retrieved assistant as a DtoAssistant object.
        """

        self.request\
            .set_method(HttpMethod.GET)\
            .add_uri_parameter(assistant_id)

        return self.client.execute_request(self.request.build(), response_hook=DtoAssistant)

    def get_assistant_file(self, assistant_id: str, assistant_file_id: str):
        """
        Retrieves a specific file for the specified assistant.

        Args:
            assistant_id: The ID of the assistant.
            assistant_file_id: The ID of the file.

        Returns:
            The retrieved file as a DtoAssistantFile object.
        """
        self.request\
            .set_method(HttpMethod.GET)\
            .add_uri_parameter(assistant_id)\
            .add_uri_parameter('files')\
            .add_uri_parameter(assistant_file_id)

        return self.client.execute_request(self.request.build(), response_hook=DtoAssistantFile)

    def update_assistant(self, assistant_id: str, payload: DtoAssistant):
        """
        Updates the specified assistant with the given payload.

        Args:
            assistant_id: The ID of the assistant.
            payload: Data transfer object containing the updated configuration.

        Returns:
            The updated assistant as a DtoAssistant object.
        """
        self.request\
            .set_method(HttpMethod.POST)\
            .add_uri_parameter(assistant_id)\
            .add_json_body(payload)\

        return self.client.execute_request(self.request.build(), response_hook=DtoAssistant)

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

        return self.client.execute_request(self.request.build(), response_hook=DtoResponseStatus)

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

        return self.client.execute_request(self.request.build(), response_hook=DtoResponseStatus)
