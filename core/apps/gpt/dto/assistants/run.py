from web.services.core.json import JsonObject
from apps.gpt.dto.assistants.common import DtoError
from apps.gpt.dto.assistants.thread import DtoThreadCreate
from typing import Optional


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
    metadata: Optional = None  # Optional metadata associated with the message.
    usage: object = None  # The usage of the run.


class DtoRunCreate(JsonObject):
    """
    DTO for a Run creation.
    """
    assistant_id: str = None  # The ID of the Assistant associated with this run.
    model: str = None  # The model used by the run.
    instructions: str = None  # Instructions for using the run.
    additional_instructions: str = None  # Additional instructions for using the run.
    tools: list = None  # A list of tools used by the run.
    metadata: Optional = None  # Optional metadata associated with the run.
    stream: Optional = None  # The stream associated with the run.


class DtoThreadRunCreate(DtoRunCreate):
    """
    DTO for a Thread Run creation.
    """
    thread: DtoThreadCreate = None  # The ID of the thread associated with this run.


class DtoRunStep(DtoRun):
    """
    DTO for a Run step detail.
    """
    step_details: Optional = None  # The details of the step.


class DtoToolInput(JsonObject):
    tool_call_id: str = None  # The ID of the tool call associated with this input.
    output: str = None  # The output associated with this input.


class DtoSubmitToolOutputs(JsonObject):
    """
    DTO for a Tool Outputs submission.
    """
    tool_outputs: list[DtoToolInput] = None
    stream: Optional = None  # The stream associated with the outputs.
