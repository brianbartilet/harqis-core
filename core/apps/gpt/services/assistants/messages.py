from core.apps.gpt.base_service import BaseServiceHarqisGPT
from core.apps.gpt.constants.http_headers import HttpHeadersGPT
from core.apps.gpt.models.assistants.message import Message, MessageFile, ListMessages, \
    ListMessageFiles, MessageCreate

from core.apps.gpt.models.assistants.common import ListQuery

from core.web.services.core.constants.http_methods import HttpMethod


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
            .add_header(HttpHeadersGPT.OPEN_API_BETA, "assistants=v2")\
            .set_base_uri('threads')

    def create_message(self, thread_id: str, payload: MessageCreate):
        """
        Creates a new message.

        Args:
            thread_id: The ID of the thread.
            payload: Data transfer object containing the message's configuration.

        Returns:
            The created message as a Message object.
        """
        request = self.request\
            .set_method(HttpMethod.POST)\
            .add_uri_parameter(thread_id) \
            .add_uri_parameter('messages') \
            .add_json_body(payload) \
            .build()

        return self.client.execute_request(request, response_hook=Message)

    def get_messages(self, thread_id: str, query=ListQuery()):
        """
        List messages from a thread

        Args:
            thread_id: The ID of the thread.
            query: query object containing the message's configuration.

        Returns:
            The created message as a Message object.
        """
        request = self.request\
            .set_method(HttpMethod.GET)\
            .add_uri_parameter(thread_id)\
            .add_uri_parameter('messages')\
            .add_query_strings(**query.get_dict())\
            .build()

        return self.client.execute_request(request, response_hook=ListMessages)

    def get_message(self, thread_id: str, message_id: str):
        """
        Get message object by ID

        Args:
            thread_id: The ID of the thread.
            message_id: The ID of the message

        Returns:
            The created message as a Message object.
        """
        request = self.request\
            .set_method(HttpMethod.GET)\
            .add_uri_parameter(thread_id)\
            .add_uri_parameter('messages')\
            .add_uri_parameter(message_id)\
            .build()

        return self.client.execute_request(request, response_hook=Message)

    def get_message_files(self, thread_id: str, message_id: str, query=ListQuery()):
        """
        List messages from a thread

        Args:
            thread_id: The ID of the thread.
            message_id: The ID of the message
            query: query object containing the message's configuration.

        Returns:
            The created message as a Message object.
        """
        request = self.request\
            .set_method(HttpMethod.GET)\
            .add_uri_parameter(thread_id)\
            .add_uri_parameter('messages')\
            .add_uri_parameter(message_id)\
            .add_query_strings(**query.get_dict())\
            .build()

        return self.client.execute_request(request, response_hook=ListMessageFiles)

    def get_message_file(self, thread_id: str, message_id: str, file_id: str):
        """
        Get message object by ID

        Args:
            thread_id: The ID of the thread.
            message_id: The ID of the message
            file_id: The ID of the file

        Returns:
            The created message as a Message object.
        """
        request = self.request\
            .set_method(HttpMethod.GET)\
            .add_uri_parameter(thread_id)\
            .add_uri_parameter('messages')\
            .add_uri_parameter(message_id) \
            .add_uri_parameter('files') \
            .add_uri_parameter(file_id) \
            .build()

        return self.client.execute_request(request, response_hook=MessageFile)

    def update_message(self, thread_id: str, message_id: str, payload: Message):
        """
        Update message object by ID

        Args:
            thread_id: The ID of the thread.
            message_id: The ID of the message
            payload: Data transfer object containing the message's configuration and
                only uses .metadata property

        Returns:
            The created message as a Message object.
        """
        request = self.request\
            .set_method(HttpMethod.GET)\
            .add_uri_parameter(thread_id)\
            .add_uri_parameter('messages')\
            .add_uri_parameter(message_id) \
            .add_json_body(payload) \
            .build()

        return self.client.execute_request(request, response_hook=Message)