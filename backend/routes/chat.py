from fastapi import APIRouter,WebSocket, WebSocketDisconnect, Request
from config.ConnectionManager import ConnectionManager
from config.BotManager import BotManager
import json

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
