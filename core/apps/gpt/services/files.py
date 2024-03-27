import os
from core.apps.gpt.base_service import BaseServiceHarqisGPT

from core.web.services.core.constants.http_methods import HttpMethod

from core.apps.gpt.dto.file import DtoFile, DtoFileStatus


class ServiceFiles(BaseServiceHarqisGPT):
    """
    Service class for interacting with the OpenAI Files API.
    https://platform.openai.com/docs/api-reference/files
    """
    def __init__(self, config):
        """
        Initializes the ServiceAssistants instance with the given configuration.

        Args:
            config: Configuration object for the service.
        """
        super(ServiceFiles, self).__init__(config)

        self.request.add_uri_parameter('files')

    def get_files(self):
        """
        Get all files.
        """
        self.request\
            .set_method(HttpMethod.GET)

        return self.native_client.files.list()

    def upload_file(self, file_name: str, base_path: str = os.getcwd()):
        """
        Uploads a new files for assistants to use

        Args:
            file_name: the file to be uploaded
            base_path: Root path to of the file
        Returns:
            The created file as a DtoAssistantFile object.
        """
        file_path = os.path.join(base_path, file_name)
        response = self.native_client.files.create(file=open(file_path, 'rb'), purpose="assistants")

        return response

    def upload_files(self, file_names: list, base_path: str = os.getcwd()):
        """
        Uploads a new files for assistants to use

        Args:
            file_names: the list of file paths
            base_path: Root path to of the file
        Returns:
            The created file as a DtoAssistantFile object.
        """
        uploaded_files = []

        for file_name in file_names:
            uploaded_files.append(self.upload_file(file_name, base_path))

        return uploaded_files

    def get_file(self, file_id: str):
        """
        Get file object by ID.

        Args:
            file_id: Target file by ID

        Returns:
            The file object
        """
        request = self.request\
            .set_method(HttpMethod.GET)\
            .add_uri_parameter(file_id) \
            .build()

        return self.client.execute_request(request, response_hook=DtoFile)

    def get_file_content(self, file_id: str, file_name: str = None, base_path: str = os.getcwd()):
        """
        Get file content by ID.

        Args:
            file_id: Target file by ID
            file_name: The file name to save the content
            base_path: Root path to save the file

        Returns:
            The file object
        """
        request = self.request\
            .set_method(HttpMethod.GET)\
            .add_uri_parameter(file_id) \
            .add_uri_parameter('content') \
            .build()

        response = self.client.execute_request(request)
        if file_name is not None:
            file_path = os.path.join(base_path, file_name)
            with open(file_path, 'wb') as file:
                file.write(response.raw_bytes)

        return response

    def delete_file(self, file_id: str):
        """
        Delete file object by ID.

        Args:
            file_id: Target file by ID.

        Returns:
            The file object deleted status
        """
        request = self.request\
            .set_method(HttpMethod.DELETE)\
            .add_uri_parameter(file_id) \
            .build()

        return self.client.execute_request(request, response_hook=DtoFileStatus)


