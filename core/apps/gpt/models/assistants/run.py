from core.web.services.core.json import JsonObject
from core.apps.gpt.models.assistants.common import Error
from core.apps.gpt.models.assistants.thread import ThreadCreate

from typing import Optional


class RequiredAction(JsonObject):
    type: str = None  # The type of the required action.
    submit_tool_outputs: object


class Run(JsonObject):
    """
    Model for a Run.
    """
    id: str = None  # The unique identifier for the Assistant.
    object: str = None  # The type of the object, should be "assistant".
    created_at: int = None  # The timestamp of when the Assistant was created.
    thread_id: str = None  # The ID of the thread associated with this run.
    assistant_id: str = None  # The ID of the Assistant associated with this run.
    status: str = None  # The status of the run.
    required_action: RequiredAction = None  # The required action for the run.
    last_error: Error = None  # The last error for the run.
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


class RunCreate(JsonObject):
    """
    Model for a Run creation.
    """
    assistant_id: str = None  # The ID of the Assistant associated with this run.
    model: Optional[str] = None  # The model used by the run.
    instructions: Optional[str] = None  # Instructions for using the run.
    additional_instructions: Optional[str] = None  # Additional instructions for using the run.
    tools: Optional[list] = None  # A list of tools used by the run.
    metadata: Optional = None  # Optional metadata associated with the run.
    stream: Optional[bool] = False  # The stream associated with the run.


class ThreadRunCreate(RunCreate):
    """
    Model for a Thread Run creation.
    """
    thread: ThreadCreate = None  # The ID of the thread associated with this run.


class RunStep(Run):
    """
    Model for a Run step detail.
    """
    step_details: Optional = None  # The details of the step.


class ToolInput(JsonObject):
    tool_call_id: str = None  # The ID of the tool call associated with this input.
    output: str = None  # The output associated with this input.


class SubmitToolOutputs(JsonObject):
    """
    Model for a Tool Outputs submission.
    """
    tool_outputs: list[ToolInput] = None
    stream: Optional = None  # The stream associated with the outputs.
