from pydantic import BaseModel

class Message(BaseModel):
    content: str

class ChatResponse(BaseModel):
    message: str
