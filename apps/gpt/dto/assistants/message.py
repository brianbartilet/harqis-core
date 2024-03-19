from web.services.core.json import JsonObject
from apps.gpt.dto.assistants.common import DtoListResponse
from typing import Optional, Any
from enum import Enum


class DtoDetails(JsonObject):
    reason: str = None  # The reason for the status.


class DtoContentImage(JsonObject):
    """
    DTO for an Image Content.
    """
    type: str = None  # The URL of the image.
    image_file = None  # The image file.


class DtoContentText(JsonObject):
    """
    DTO for a Text Content.
    """
    type: str = None  # The type of the content.
    text: str = None  # The text content.


class DtoContent(Enum):
    IMAGE = DtoContentImage
    TEXT = DtoContentText


class DtoMessage(JsonObject):
    """
    DTO for a Message.
    """
    id: str = None  # The unique identifier for the Assistant.
    object: str = None  # The type of the object, should be "assistant".
    created_at: int = None  # The timestamp of when the Assistant was created.
    thread_id: str  # The ID of the thread associated with this message.
    status: str = None  # The status of the message.
    incomplete_details: DtoDetails = None  # The reason for the status.
    completed_at: int = None  # The timestamp of when the message was completed.
    incomplete_at: int = None  # The timestamp of when the message was marked as incomplete.
    role: str = 'user'  # The role of the message.
    content: Any = None  # The content of the message.
    assistant_id: str = None  # The ID of the Assistant associated with this message.
    run_id: str = None  # The ID of the run associated with this message.
    metadata: Optional = None  # Optional metadata associated with the message.


class DtoMessageCreate(JsonObject):
    role: str = 'user'  # The role of the message.
    content: Any = None  # The content of the message.
    file_ids: Optional = []
    metadata: Optional = None  # Optional metadata associated with the message.


class DtoMessageFile(JsonObject):
    """
    DTO for a Message File.
    """
    id: str = None  # The ID of the message associated with this file.
    object: str = None  # The type of the object
    created_at: int = None  # The timestamp of when the message was created.
    message_id: str = None  # The ID of the message associated with this file.
    file_id: str = None  # The ID of the file associated with this message.


class DtoListMessages(DtoListResponse):
    """
    DTO for an Assistant Response.
    """
    data: list[DtoMessage] = None  # A list of Message DTOs in the response.


class DtoListMessageFiles(DtoListResponse):
    """
    DTO for an Assistant Response.
    """
    data: list[DtoMessageFile] = None  # A list of Message DTOs in the response.
