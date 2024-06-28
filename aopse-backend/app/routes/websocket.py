import asyncio

from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from pydantic import ValidationError
import json

from app.models import EventType, ChatResponse, WebSocketMessage, Message
from app.services.ai_service import AIService

router = APIRouter()


@router.websocket("/ws/chat")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    ai_service = AIService()
    stream_task = None

    try:
        while True:
            try:
                data = await websocket.receive_text()
                event = WebSocketMessage.parse_raw(data)

                if event.event == EventType.SEND_MESSAGE:
                    if not isinstance(event.data, Message):
                        raise ValidationError("Invalid data type for SEND_MESSAGE event")

                    message = event.data

                    if stream_task:
                        stream_task.cancel()
                        try:
                            await stream_task
                        except asyncio.CancelledError:
                            pass

                    stream_task = asyncio.create_task(stream_response(websocket, ai_service, message.content))

                elif event.event == EventType.ABORT:
                    if stream_task:
                        stream_task.cancel()
                        try:
                            await stream_task
                        except asyncio.CancelledError:
                            pass
                    await websocket.send_text(WebSocketMessage(
                        event=EventType.ABORT,
                        data=ChatResponse(message="Stream aborted")
                    ).json())

                else:
                    await websocket.send_text(WebSocketMessage(
                        event=EventType.UNKNOWN_EVENT,
                        data=ChatResponse(message="Unknown event type")
                    ).json())

            except json.JSONDecodeError:
                await websocket.send_text(WebSocketMessage(
                    event=EventType.SYNTAX_ERROR,
                    data=ChatResponse(message="Invalid JSON")
                ).json())
            except ValidationError as e:
                await websocket.send_text(WebSocketMessage(
                    event=EventType.SYNTAX_ERROR,
                    data=ChatResponse(message=f"Invalid message structure: {str(e)}")
                ).json())

    except WebSocketDisconnect:
        if stream_task:
            stream_task.cancel()
        await websocket.close()


async def stream_response(websocket: WebSocket, ai_service: AIService, content: str):
    try:
        async for chunk in ai_service.stream_response(content):
            response_event = WebSocketMessage(
                event=EventType.RECEIVE_RESPONSE,
                data=ChatResponse(message=chunk)
            )
            await websocket.send_text(response_event.json())
    except asyncio.CancelledError:
        # TODO: Handle cancellation if needed
        pass