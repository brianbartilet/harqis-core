from web.services.core.json import JsonObject
from apps.gpt.dto.assistants.common import DtoError
from typing import TypeVar

TMetaData = TypeVar("TMetaData")


class DtoRequiredAction(JsonObject):
    type: str = None  # The type of the required action.
    submit_tool_outputs: object


class DtoRun(JsonObject):
    """
    DTO for a Run.
    """
    id: str = None  # The unique identifier for the Assistant.
    object: str = None  # The type of the object, should be "assistant".
    created_at: int = None  # The timestamp of when the Assistant was created.
    thread_id: str = None  # The ID of the thread associated with this run.
    assistant_id: str = None  # The ID of the Assistant associated with this run.
    status: str = None  # The status of the run.
    required_action: DtoRequiredAction = None  # The required action for the run.
    last_error: DtoError = None  # The last error for the run.
    expired_at: int = None  # The timestamp of when the run will expire.
    started_at: int = None  # The timestamp of when the run was started.
    cancelled_at: int = None  # The timestamp of when the run was cancelled.
    failed_at: int = None  # The timestamp of when the run failed.
    completed_at: int = None  # The timestamp of when the run was completed.
    model: str = None  # The model used by the run.
    instructions: str = None  # Instructions for using the run.
    tools: list = None  # A list of tools used by the run.
    file_ids: list = None  # A list of file IDs associated with the run.
    metadata: TMetaData = None  # Optional metadata associated with the message.
    usage: object = None  # The usage of the run.


class DtoRunStep(DtoRun):
    """
    DTO for a Run step detail.
    """
    step_details: TMetaData = None  # The details of the step.
