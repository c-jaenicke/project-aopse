from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from app.services.ai_service import AIService

router = APIRouter()


@router.websocket("/ws/chat")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    ai_service = AIService()
    try:
        while True:
            message = await websocket.receive_text()
            async for chunk in ai_service.stream_response(message):
                await websocket.send_text(chunk)
    except WebSocketDisconnect:
        await websocket.close()
