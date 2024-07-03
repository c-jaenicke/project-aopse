from pydantic import BaseModel
from enum import Enum
from typing import Optional, Dict, Any, Union


class EventType(str, Enum):
    CLIENT_MESSAGE = "client_message"
    CLIENT_ABORT = "client_abort"
    CLIENT_INITIATE_THREAD = "client_initiate_thread"
    CLIENT_CHANGE_MODEL = "client_change_model"
    SERVER_CHANGE_MODEL = "server_change_model"
    SERVER_AI_RESPONSE = "server_ai_response"
    SERVER_SEND_THREAD = "server_send_thread"
    SERVER_ABORT = "server_abort"
    SERVER_ERROR = "server_error"
    SERVER_AI_STATUS = "server_ai_status"
    SERVER_TOOL_CALL = "server_tool_call"
    SERVER_REQUIRES_ACTION = "server_requires_action"


class ClientMessage(BaseModel):
    thread_id: str
    content: Optional[str] = None


class AIResponseStatus(str, Enum):
    streaming = "streaming"
    completed = "completed"
    aborted = "aborted"


class AIRunStatus(str, Enum):
    queued = "queued"
    in_progress = "in_progress"
    completed = "completed"
    requires_action = "requires_action"
    expired = "expired"
    cancelling = "cancelling"
    cancelled = "cancelled"
    failed = "failed"
    incomplete = "incomplete"


class ServerResponse(BaseModel):
    status: Optional[AIResponseStatus] = None
    content: str
    run_status: Optional[AIRunStatus] = None
    metadata: Optional[Dict[str, Any]] = None


class WebSocketMessage(BaseModel):
    event: EventType
    data: Optional[Union[ClientMessage, ServerResponse]] = None
