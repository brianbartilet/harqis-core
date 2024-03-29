from core.web.services.core.json import JsonObject
from core.apps.gpt.models.assistants.common import ListResponse
from typing import Optional


class Assistant(JsonObject):
    """
    Model for an Assistant.
    """
    id: str = None  # The unique identifier for the Assistant.
    object: str = None  # The type of the object, should be "assistant".
    created_at: int = None  # The timestamp of when the Assistant was created.
    name: str = None  # The name of the Assistant.
    description: str = None  # A brief description of the Assistant.
    model: str = None  # The model used by the Assistant.
    instructions: str = None  # Instructions for using the Assistant.
    tools: [] = None  # A list of tools used by the Assistant.
    file_ids: [] = None  # A list of file IDs associated with the Assistant.
    metadata: Optional = None  # Optional metadata associated with the Assistant.


class AssistantFile(JsonObject):
    """
    Model for an Assistant File.
    """
    id: str = None  # The unique identifier for the Assistant File.
    object: str = None  # The type of the object, should be "assistant_file".
    created_at: int = None  # The timestamp of when the Assistant File was created.
    assistant_id: str = None  # The ID of the Assistant associated with this file.


class ListAssistants(ListResponse):
    """
    Model for an Assistant Response.
    """
    data: list[Assistant] = None  # A list of Assistant Models in the response.



