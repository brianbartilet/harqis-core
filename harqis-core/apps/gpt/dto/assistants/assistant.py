from web.services.core.json import JsonObject
from apps.gpt.dto.assistants.common import DtoListResponse
from typing import Optional


class DtoAssistant(JsonObject):
    """
    DTO for an Assistant.
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


class DtoAssistantFile(JsonObject):
    """
    DTO for an Assistant File.
    """
    id: str = None  # The unique identifier for the Assistant File.
    object: str = None  # The type of the object, should be "assistant_file".
    created_at: int = None  # The timestamp of when the Assistant File was created.
    assistant_id: str = None  # The ID of the Assistant associated with this file.


class DtoListAssistants(DtoListResponse):
    """
    DTO for an Assistant Response.
    """
    data: list[DtoAssistant] = None  # A list of Assistant DTOs in the response.



