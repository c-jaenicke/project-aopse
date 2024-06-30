from pydantic import BaseModel
from enum import Enum


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


class ClientMessage(BaseModel):
    thread_id: str
    content: str | None = None


class AIResponseStatus(str, Enum):
    streaming = "streaming"
    completed = "completed"
    aborted = "aborted"


class ServerResponse(BaseModel):
    status: AIResponseStatus | None = None
    content: str


class WebSocketMessage(BaseModel):
    event: EventType
    data: ClientMessage | ServerResponse | None = None
