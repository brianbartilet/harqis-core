from core.apps.gpt.models.assistants.message import Message
from core.web.services.core.json import JsonObject

from typing import Optional, Iterable


class Thread(JsonObject):
    """
    Model for a Thread.
    """
    id: str = None  # The unique identifier for the Assistant.
    object: str = 'assistant'  # The type of the object, should be "assistant".
    created_at: int = None  # The timestamp of when the Assistant was created.
    metadata: Optional = None  # Optional metadata associated with the Assistant.


class ThreadCreate(JsonObject):
    """
    Model for a Thread creation.
    """
    messages: Optional[Iterable[Message]] = None  # A list of messages to be created with the thread.
    metadata: Optional = None  # Optional metadata associated with the Assistant.

