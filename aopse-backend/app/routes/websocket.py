import asyncio

from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from pydantic import ValidationError
import json

from app.models import EventType, ClientMessage, AIResponseStatus, ServerResponse, WebSocketMessage
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

                if event.event == EventType.CLIENT_MESSAGE:
                    if not isinstance(event.data, ClientMessage):
                        raise ValidationError("Invalid data type for CLIENT_MESSAGE event")

                    message = event.data

                    if stream_task:
                        stream_task.cancel()
                        try:
                            await stream_task
                        except asyncio.CancelledError:
                            pass

                    stream_task = asyncio.create_task(stream_response(websocket, ai_service, message.content))

                elif event.event == EventType.CLIENT_ABORT:
                    if stream_task:
                        stream_task.cancel()
                        try:
                            await stream_task
                        except asyncio.CancelledError:
                            pass
                    await websocket.send_text(WebSocketMessage(
                        event=EventType.SERVER_ABORT,
                        data=ServerResponse(status=AIResponseStatus.aborted, content="aborted by client")
                    ).json())

                else:
                    await websocket.send_text(WebSocketMessage(
                        event=EventType.SERVER_ERROR,
                        data=ServerResponse(content="Invalid event type")
                    ).json())

            except json.JSONDecodeError:
                await websocket.send_text(WebSocketMessage(
                    event=EventType.SERVER_ERROR,
                    data=ServerResponse(content="Invalid JSON")
                ).json())
            except ValidationError as e:
                await websocket.send_text(WebSocketMessage(
                    event=EventType.SERVER_ERROR,
                    data=ServerResponse(content=str(e))
                ).json())

    except WebSocketDisconnect:
        if stream_task:
            stream_task.cancel()
        await websocket.close()


async def stream_response(websocket: WebSocket, ai_service: AIService, content: str):
    try:
        async for chunk in ai_service.stream_response(content):
            response_event = WebSocketMessage(
                event=EventType.SERVER_AI_RESPONSE,
                data=ServerResponse(content=chunk, status=AIResponseStatus.streaming)
            )
            await websocket.send_text(response_event.json())

        response_event = WebSocketMessage(
            event=EventType.SERVER_AI_RESPONSE,
            data=ServerResponse(content="", status=AIResponseStatus.completed)
        )
        await websocket.send_text(response_event.json())
    except asyncio.CancelledError:
        pass
