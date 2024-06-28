from pydantic import BaseModel
from enum import Enum


class EventType(str, Enum):
    SEND_MESSAGE = "send_message"
    RECEIVE_RESPONSE = "receive_response"
    ABORT = "abort"
    SYNTAX_ERROR = "syntax_error"
    UNKNOWN_EVENT = "unknown_event"


class Message(BaseModel):
    content: str


class ChatResponse(BaseModel):
    message: str


class WebSocketMessage(BaseModel):
    event: EventType
    data: Message | ChatResponse | None = None
