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

    try:
        while True:
            try:
                data = await websocket.receive_text()
                event = WebSocketMessage.parse_raw(data)

                if event.event == EventType.CLIENT_INITIATE_THREAD:
                    thread_id = ai_service.create_thread()
                    await websocket.send_text(
                        WebSocketMessage(
                            event=EventType.SERVER_SEND_THREAD,
                            data=ServerResponse(content=thread_id)
                        ).json()
                    )
                elif event.event == EventType.CLIENT_MESSAGE:
                    if not isinstance(event.data, ClientMessage):
                        raise ValidationError("Invalid data type for CLIENT_MESSAGE event")

                    message = event.data
                    asyncio.create_task(
                        run_in_executor(ai_service.stream_response, message.thread_id, message.content, websocket)
                    )
                elif event.event == EventType.CLIENT_ABORT:
                    await websocket.send_text(
                        WebSocketMessage(
                            event=EventType.SERVER_ABORT,
                            data=ServerResponse(status=AIResponseStatus.aborted, content="aborted by client")
                        ).json()
                    )
                else:
                    await websocket.send_text(
                        WebSocketMessage(
                            event=EventType.SERVER_ERROR,
                            data=ServerResponse(content="Invalid event type")
                        ).json()
                    )
            except WebSocketDisconnect:
                break
            except json.JSONDecodeError:
                await websocket.send_text(
                    WebSocketMessage(
                        event=EventType.SERVER_ERROR,
                        data=ServerResponse(content="Invalid JSON")
                    ).json()
                )
            except ValidationError as e:
                await websocket.send_text(
                    WebSocketMessage(
                        event=EventType.SERVER_ERROR,
                        data=ServerResponse(content=str(e))
                    ).json()
                )
    except WebSocketDisconnect:
        pass
    except RuntimeError as e:
        if str(e) == "Unexpected ASGI message 'websocket.close', after sending 'websocket.close' or response already completed":
            pass
        else:
            raise
    finally:
        try:
            await websocket.close()
        except RuntimeError as e:
            if str(e) == "Unexpected ASGI message 'websocket.close', after sending 'websocket.close' or response already completed":
                pass
            else:
                raise


async def run_in_executor(func, *args):
    loop = asyncio.get_event_loop()
    await loop.run_in_executor(None, func, *args)


async def stream_response(websocket: WebSocket, ai_service: AIService, thread_id: str, content: str):
    try:
        async for chunk in ai_service.stream_response(thread_id, content):
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
