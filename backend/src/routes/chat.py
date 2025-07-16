import uuid
from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Request, HTTPException
from fastapi.responses import StreamingResponse
from src.services.bot_service import BotManager
from src.services.websocket_service import ConnectionManager
import json
from ollama import AsyncClient
from pydantic import BaseModel
import asyncio
import base64

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
            print(chunk['message']['content'])  # Debugging output
            yield chunk['message']['content']

    return StreamingResponse(
        generate(),
        media_type="text/plain" # This remains text/plain if you just stream raw text deltas
    )

@router.post("/custom-ai-chat-protocol-data")
async def chat_data_stream_endpoint():
        async def generate_data_stream():
            delay = 0.05  # Streaming delay for simulation
            message_id = str(uuid.uuid4())

            # Message Start Part
            yield f'data:{json.dumps({"type":"start","messageId": message_id})}\n\n'
            await asyncio.sleep(delay)

            # Text Block 1
            text_id1 = str(uuid.uuid4())
            yield f'data:{json.dumps({"type":"text-start","id": text_id1})}\n\n'
            await asyncio.sleep(delay)
            yield f'data:{json.dumps({"type":"text-delta","id": text_id1,"delta":"Hello!"})}\n\n'
            await asyncio.sleep(delay)
            yield f'data:{json.dumps({"type":"text-delta","id": text_id1,"delta":" This is the initial text. "})}\n\n'
            await asyncio.sleep(delay)
            yield f'data:{json.dumps({"type":"text-end","id": text_id1})}\n\n'
            await asyncio.sleep(delay)

            # Text Block 2
            text_id2 = str(uuid.uuid4())
            yield f'data:{json.dumps({"type":"text-start","id": text_id2})}\n\n'
            await asyncio.sleep(delay)
            yield f'data:{json.dumps({"type":"text-delta","id": text_id2,"delta":"Here is some more text."})}\n\n'
            await asyncio.sleep(delay)
            yield f'data:{json.dumps({"type":"text-end","id": text_id2})}\n\n'
            await asyncio.sleep(delay)

            # Start Step Part
            yield f'data:{json.dumps({"type":"start-step"})}\n\n'
            await asyncio.sleep(delay)

            # Reasoning Block
            reasoning_id = str(uuid.uuid4())
            yield f'data:{json.dumps({"type":"reasoning-start","id": reasoning_id})}\n\n'
            await asyncio.sleep(delay)
            yield f'data:{json.dumps({"type":"reasoning-delta","id": reasoning_id,"delta":"Okay, planning the first step..."})}\n\n'
            await asyncio.sleep(delay)
            yield f'data:{json.dumps({"type":"reasoning-delta","id": reasoning_id,"delta":" I will now search for relevant information."})}\n\n'
            await asyncio.sleep(delay)
            yield f'data:{json.dumps({"type":"reasoning-end","id": reasoning_id})}\n\n'
            await asyncio.sleep(delay)

            # Text Block 3
            text_id3 = str(uuid.uuid4())
            yield f'data:{json.dumps({"type":"text-start","id": text_id3})}\n\n'
            await asyncio.sleep(delay)
            yield f'data:{json.dumps({"type":"text-delta","id": text_id3,"delta":"Here is 2 some more text."})}\n\n'
            await asyncio.sleep(delay)
            yield f'data:{json.dumps({"type":"text-end","id": text_id3})}\n\n'
            await asyncio.sleep(delay)

            # Source URL Part
            yield f'data:{json.dumps({"type":"source-url","sourceId":"src-1","url":"https://vercel.com/docs"})}\n\n'
            await asyncio.sleep(delay)

            # File Part (using URL instead of base64 content)
            yield f'data:{json.dumps({"type":"file","url":"https://example.com/file.txt","mediaType":"text/plain"})}\n\n'
            await asyncio.sleep(delay)

            # Data Parts with custom types
            yield f'data:{json.dumps({"type":"data-search-status","data":{"status":"Searching...","query":1}})}\n\n'
            await asyncio.sleep(delay)
            yield f'data:{json.dumps({"type":"data-search-results","data":{"results_found":5}})}\n\n'
            await asyncio.sleep(delay)

            # Error Part
            yield f'data:{json.dumps({"type":"error","errorText":"Encountered a minor issue during search, but continuing."})}\n\n'
            await asyncio.sleep(delay)

            # Streaming Tool Call
            tool_call_id_stream = "call_stream_weather_123"
            tool_name_stream = "get_current_weather_streaming"
            yield f'data:{json.dumps({"type":"tool-input-start","toolCallId":tool_call_id_stream,"toolName":tool_name_stream})}\n\n'
            await asyncio.sleep(delay)
            yield f'data:{json.dumps({"type":"tool-input-delta","toolCallId":tool_call_id_stream,"inputTextDelta":"{\"location\": "})}\n\n'
            await asyncio.sleep(0.1)
            yield f'data:{json.dumps({"type":"tool-input-delta","toolCallId":tool_call_id_stream,"inputTextDelta":"\"Tunis, TN\"}"})}\n\n'
            await asyncio.sleep(0.1)
            yield f'data:{json.dumps({"type":"tool-input-available","toolCallId":tool_call_id_stream,"toolName":tool_name_stream,"input":{"location":"Tunis, TN"}})}\n\n'
            await asyncio.sleep(delay)
            yield f'data:{json.dumps({"type":"tool-output-available","toolCallId":tool_call_id_stream,"output":{"temperature":"25C","condition":"Sunny"}})}\n\n'
            await asyncio.sleep(delay)

            # Non-Streaming Tool Call
            tool_call_id_nonstream = "call_nonstream_user_456"
            tool_name_nonstream = "lookup_user_info"
            yield f'data:{json.dumps({"type":"tool-input-available","toolCallId":tool_call_id_nonstream,"toolName":tool_name_nonstream,"input":{"user_id":"usr_abc"}})}\n\n'
            await asyncio.sleep(delay)
            yield f'data:{json.dumps({"type":"tool-output-available","toolCallId":tool_call_id_nonstream,"output":{"name":"John Doe","status":"Active"}})}\n\n'
            await asyncio.sleep(delay)

            # Finish Step Part
            yield f'data:{json.dumps({"type":"finish-step","finishReason":"tool-calls","usage":{"promptTokens":50,"completionTokens":75},"isContinued":False})}\n\n'
            await asyncio.sleep(delay)

            # Finish Message Part and Stream Termination
            yield f'data:{json.dumps({"type":"finish"})}\n\n'
            yield 'data: [DONE]\n\n'

        return StreamingResponse(
            generate_data_stream(),
            media_type="text/event-stream",
            headers={
                'x-vercel-ai-ui-message-stream': 'v1',
                'Cache-Control': 'no-cache',
                'Connection': 'keep-alive'
            }
        )