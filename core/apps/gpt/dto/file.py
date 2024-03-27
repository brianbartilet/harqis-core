from core.web.services.core.json import JsonObject
from core.apps.gpt.dto.assistants.common import DtoListResponse
from typing import Optional, Any


class DtoFileUpload(JsonObject):
    """
    DTO for uploading a file.
    """
    file: bytes = None
    purpose: str = None


class DtoFile(JsonObject):
    """
    DTO for a file object.
    """
    id: str = None  # The unique identifier for the file.
    bytes: int = None  # Amount of bytes in the file.
    created_at: int = None  # The timestamp of when the file was uploaded.
    filename: str = None  # The name of the file.
    object: str = None  # The object type, should be "file".
    purpose: str = None  # The purpose of the file.


class DtoFileStatus(JsonObject):
    id: str = None
    object: str = None
    deleted: bool = None
