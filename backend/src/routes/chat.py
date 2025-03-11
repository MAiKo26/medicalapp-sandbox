from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Request, HTTPException
from fastapi.responses import StreamingResponse
from src.services.bot_service import BotManager
from src.services.websocket_service import ConnectionManager
import json
from ollama import AsyncClient
from pydantic import BaseModel


manager = ConnectionManager()

router = APIRouter(prefix="/ws/chat")
bot = BotManager()

@router.websocket("/general/{username}")
async def websocket_connection(websocket: WebSocket, username: str):
    await manager.connect(websocket, "general")
    await manager.broadcast(json.dumps({"sender": username, "content" : f"{username} joined the general chat"}),"general")
    try:
        while True:
            data = await websocket.receive_text()
            await manager.broadcast(json.dumps({"sender": username, "content" :data}), "general")
    except WebSocketDisconnect:
        manager.disconnect(websocket, "general")
        await manager.broadcast(json.dumps({"sender": "Bot", "content" :f"{username} left the general chat"}), "general")


@router.websocket("/bot/{username}")
async def websocket_connection(websocket: WebSocket, username: str):
    await manager.connect(websocket, f"bot+{username}")
    await manager.broadcast(json.dumps({"sender": "Bot", "content" :f"Welcome {username}! how can I help you ?"}), f"bot+{username}")
    try:
        while True:
            data = await websocket.receive_text()
            await manager.broadcast(json.dumps({"sender": username, "content" :data}), f"bot+{username}")
            botreply = await bot.reply(data)
            await manager.broadcast(json.dumps({"sender": "Bot", "content" :f"{botreply}"}), f"bot+{username}")
    except WebSocketDisconnect:
        manager.disconnect(websocket, f"bot+{username}")





class Message(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    messages: list[Message]

@router.post("/ai-chat")
async def chat_endpoint(chat_request: ChatRequest):
    client = AsyncClient()
    messages = [msg.dict() for msg in chat_request.messages]



    response = await client.chat(
        model='huggingface.co/Omartificial-Intelligence-Space/ALLaM-7B-Instruct-preview-Q4_K_M-GGUF:latest',
        messages=messages,
        stream=True
    )


    async def generate():
        async for chunk in response:
            yield chunk['message']['content']

    
    return StreamingResponse(
        generate(),
        media_type="text/plain"
    )