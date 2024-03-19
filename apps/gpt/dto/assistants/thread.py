from apps.gpt.dto.assistants.message import DtoMessage
from web.services.core.json import JsonObject
from typing import Optional


class DtoThread(JsonObject):
    """
    DTO for a Thread.
    """
    id: str = None  # The unique identifier for the Assistant.
    object: str = 'assistant'  # The type of the object, should be "assistant".
    created_at: int = None  # The timestamp of when the Assistant was created.
    metadata: Optional = None  # Optional metadata associated with the Assistant.


class DtoThreadCreate(JsonObject):
    """
    DTO for a Thread creation.
    """
    messages: list[DtoMessage] = None  # A list of messages to be created with the thread.
    metadata: Optional = None  # Optional metadata associated with the Assistant.

