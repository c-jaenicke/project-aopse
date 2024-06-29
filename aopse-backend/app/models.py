from pydantic import BaseModel
from enum import Enum


class EventType(str, Enum):
    CLIENT_MESSAGE = "client_message"
    CLIENT_ABORT = "client_abort"
    CLIENT_INITIATE_THREAD = "client_initiate_thread"
    SERVER_AI_RESPONSE = "server_ai_response"
    SERVER_SEND_THREAD = "server_send_thread"
    SERVER_ABORT = "server_abort"
    SERVER_ERROR = "server_error"


class ClientMessage(BaseModel):
    thread_id: str
    content: str


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
