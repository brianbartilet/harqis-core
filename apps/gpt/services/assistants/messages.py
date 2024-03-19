from apps.gpt.base import BaseServiceHarqisGPT
from apps.gpt.constants.http_headers import HttpHeadersGPT
from apps.gpt.dto.assistants.message import DtoMessage, DtoMessageFile, DtoListMessages, \
    DtoListMessageFiles, DtoMessageCreate
from apps.gpt.dto.assistants.common import DtoListQuery

from web.services.core.constants.http_methods import HttpMethod


class ServiceMessages(BaseServiceHarqisGPT):
    """
    Service class for interacting with the OpenAI Assistants API.
    https://platform.openai.com/docs/api-reference/messages
    """
    def __init__(self, config):
        """
        Initializes the ServiceMessages instance with the given configuration.

        Args:
            config: Configuration object for the service.
        """
        super(ServiceMessages, self).__init__(config)
        self.request\
            .add_header(HttpHeadersGPT.OPEN_API_BETA, "assistants=v1")\
            .add_uri_parameter('threads')

    def create_message(self, thread_id: str, payload: DtoMessageCreate):
        """
        Creates a new message.

        Args:
            thread_id: The ID of the thread.
            payload: Data transfer object containing the message's configuration.

        Returns:
            The created message as a DtoMessage object.
        """
        request = self.request\
            .set_method(HttpMethod.POST)\
            .add_uri_parameter(thread_id)\
            .add_json_body(payload) \
            .add_uri_parameter('messages')\
            .build()

        return self.client.execute_request(request, response_hook=DtoMessage)

    def get_messages(self, thread_id: str, query=DtoListQuery()):
        """
        List messages from a thread

        Args:
            thread_id: The ID of the thread.
            query: query object containing the message's configuration.

        Returns:
            The created message as a DtoMessage object.
        """
        request = self.request\
            .set_method(HttpMethod.GET)\
            .add_uri_parameter(thread_id)\
            .add_uri_parameter('messages')\
            .add_query_strings(**query.get_dict())\
            .build()

        return self.client.execute_request(request, response_hook=DtoListMessages)

    def get_message(self, thread_id: str, message_id: str):
        """
        Get message object by ID

        Args:
            thread_id: The ID of the thread.
            message_id: The ID of the message

        Returns:
            The created message as a DtoMessage object.
        """
        request = self.request\
            .set_method(HttpMethod.GET)\
            .add_uri_parameter(thread_id)\
            .add_uri_parameter('messages')\
            .add_uri_parameter(message_id)\
            .build()

        return self.client.execute_request(request, response_hook=DtoMessage)

    def get_message_files(self, thread_id: str, message_id: str, query=DtoListQuery()):
        """
        List messages from a thread

        Args:
            thread_id: The ID of the thread.
            message_id: The ID of the message
            query: query object containing the message's configuration.

        Returns:
            The created message as a DtoMessage object.
        """
        request = self.request\
            .set_method(HttpMethod.GET)\
            .add_uri_parameter(thread_id)\
            .add_uri_parameter('messages')\
            .add_uri_parameter(message_id)\
            .add_query_strings(**query.get_dict())\
            .build()

        return self.client.execute_request(request, response_hook=DtoListMessageFiles)

    def get_message_file(self, thread_id: str, message_id: str, file_id: str):
        """
        Get message object by ID

        Args:
            thread_id: The ID of the thread.
            message_id: The ID of the message
            file_id: The ID of the file

        Returns:
            The created message as a DtoMessage object.
        """
        request = self.request\
            .set_method(HttpMethod.GET)\
            .add_uri_parameter(thread_id)\
            .add_uri_parameter('messages')\
            .add_uri_parameter(message_id) \
            .add_uri_parameter('files') \
            .add_uri_parameter(file_id) \
            .build()

        return self.client.execute_request(request, response_hook=DtoMessageFile)

    def update_message(self, thread_id: str, message_id: str, payload: DtoMessage):
        """
        Update message object by ID

        Args:
            thread_id: The ID of the thread.
            message_id: The ID of the message
            payload: Data transfer object containing the message's configuration and
                only uses .metadata property

        Returns:
            The created message as a DtoMessage object.
        """
        request = self.request\
            .set_method(HttpMethod.GET)\
            .add_uri_parameter(thread_id)\
            .add_uri_parameter('messages')\
            .add_uri_parameter(message_id) \
            .add_json_body(payload) \
            .build()

        return self.client.execute_request(request, response_hook=DtoMessage)