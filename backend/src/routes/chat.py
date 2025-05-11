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
            yield chunk['message']['content']

    
    return StreamingResponse(
        generate(),
        media_type="text/plain"
    )

@router.post("/custom-ai-chat-protocol-data") # Use this if using FastAPI directly
async def chat_data_stream_endpoint(chat_request: ChatRequest): # Add request body if needed

    async def generate_data_stream():
        # Simulate processing time / streaming delay
        delay = 0.5

        # 0: Text Part
        text_content = "Hello! This is the initial text. "
        yield f'0:{json.dumps(text_content)}\n'
        await asyncio.sleep(delay)
        text_content_more = "Here is some more text."
        yield f'0:{json.dumps(text_content_more)}\n'
        await asyncio.sleep(delay)

        # f: Start Step Part (Optional, useful for multi-step processes)
        yield f'f:{json.dumps({"messageId": "step-1"})}\n'
        await asyncio.sleep(delay)

        # g: Reasoning Part
        yield f'g:{json.dumps("Okay")}\n'
        await asyncio.sleep(delay)
        yield f'g:{json.dumps("planning")}\n'
        await asyncio.sleep(delay)
        yield f'g:{json.dumps("the")}\n'
        await asyncio.sleep(delay)
        yield f'g:{json.dumps("first")}\n'
        await asyncio.sleep(delay)
        yield f'g:{json.dumps("step...")}\n'
        await asyncio.sleep(delay)
        yield f'g:{json.dumps(" I will now search for relevant information.")}\n'
        await asyncio.sleep(delay)

        # 8: Message Annotation Part
        yield f'8:{json.dumps([{"type": "citation", "id": "anno-1", "text": "Source [1]", "details": {"sourceId": "src-1"}}])}\n'
        yield f'8:{json.dumps([{"type51": "citation", "id": "anno-1", "text": "Source [1]", "details": {"sourceId": "src-1"}}])}\n'


        # i: Redacted Reasoning Part
        yield f'i:{json.dumps({"data": "[REDACTED: Potentially sensitive internal thought process]"})}\n'
        await asyncio.sleep(delay)

        # j: Reasoning Signature Part (Hypothetical example)
        yield f'j:{json.dumps({"signature": "sig_aBcDeF12345"})}\n'
        await asyncio.sleep(delay)

        # h: Source Part
        yield f'h:{json.dumps({"sourceType": "url", "id": "src-1", "url": "https://vercel.com/docs", "title": "Vercel Documentation"})}\n'
        await asyncio.sleep(delay)
        yield f'h:{json.dumps({"sourceType": "text", "id": "src-2", "content": "Internal knowledge base article #42"})}\n'
        await asyncio.sleep(delay)

        # k: File Part (Example: a small text file encoded)
        # file_content = "This is the content of the file."
        # file_data_base64 = base64.b64encode(file_content.encode()).decode()
        # yield f'k:{json.dumps({"data": file_data_base64, "mimeType": "text/plain;charset=utf-8"})}\n' # Specify charset
        # await asyncio.sleep(delay)

        # 2: Data Part (Arbitrary JSON data)
        yield f'2:{json.dumps([{"status": "Searching..."}, {"query": chat_request.prompt}])}\n' # Using input prompt
        await asyncio.sleep(delay)
        yield f'2:{json.dumps([{"results_found": 5}])}\n'
        await asyncio.sleep(delay)


        # 3: Error Part (Simulating an error)
        yield f'3:{json.dumps("Encountered a minor issue during search, but continuing.")}\n'
        await asyncio.sleep(delay)

        # ---- Tool Call Example (Streaming) ----
        tool_call_id_stream = "call_stream_weather_123"
        tool_name_stream = "get_current_weather_streaming"
        # b: Tool Call Streaming Start Part
        yield f'b:{json.dumps({"toolCallId": tool_call_id_stream, "toolName": tool_name_stream})}\n'
        await asyncio.sleep(delay)
        # c: Tool Call Delta Part(s)
        yield f'c:{json.dumps({"toolCallId": tool_call_id_stream, "argsTextDelta": '{"loc'})}\n'
        await asyncio.sleep(0.1)
        yield f'c:{json.dumps({"toolCallId": tool_call_id_stream, "argsTextDelta": 'ation"'})}\n'
        await asyncio.sleep(0.1)
        yield f'c:{json.dumps({"toolCallId": tool_call_id_stream, "argsTextDelta": ': "Tun'})}\n'
        await asyncio.sleep(0.1)
        yield f'c:{json.dumps({"toolCallId": tool_call_id_stream, "argsTextDelta": 'is, '})}\n'
        await asyncio.sleep(0.1)
        yield f'c:{json.dumps({"toolCallId": tool_call_id_stream, "argsTextDelta": 'TN"}'})}\n'
        await asyncio.sleep(delay)
        # 9: Tool Call Part (Needs to come *after* streaming deltas for the same call)
        yield f'9:{json.dumps({"toolCallId": tool_call_id_stream, "toolName": tool_name_stream, "args": {"location": "Tunis, TN"}})}\n'
        await asyncio.sleep(delay)
        # a: Tool Result Part
        yield f'a:{json.dumps({"toolCallId": tool_call_id_stream, "result": {"temperature": "25C", "condition": "Sunny"}})}\n'
        await asyncio.sleep(delay)
        # ---- End Tool Call Example (Streaming) ----

        # ---- Tool Call Example (Non-Streaming) ----
        tool_call_id_nonstream = "call_nonstream_user_456"
        tool_name_nonstream = "lookup_user_info"
        # 9: Tool Call Part (Sent directly)
        yield f'9:{json.dumps({"toolCallId": tool_call_id_nonstream, "toolName": tool_name_nonstream, "args": {"user_id": "usr_abc"}})}\n'
        await asyncio.sleep(delay)
        # a: Tool Result Part
        yield f'a:{json.dumps({"toolCallId": tool_call_id_nonstream, "result": {"name": "John Doe", "status": "Active"}})}\n'
        await asyncio.sleep(delay)
        # ---- End Tool Call Example (Non-Streaming) ----

        # e: Finish Step Part (Finishing the first logical step)
        yield f'e:{json.dumps({"finishReason": "tool-calls", "usage": {"promptTokens": 50, "completionTokens": 75}, "isContinued": False})}\n' # Or True if more steps follow naturally
        await asyncio.sleep(delay)

        # Optionally start another step if needed
        # yield f'f:{json.dumps({"messageId": "step-2"})}\n'
        # ... more parts ...
        # yield f'e:{json.dumps({"finishReason": "stop", "usage": {"promptTokens": 10, "completionTokens": 20}, "isContinued": False})}\n'

        # d: Finish Message Part (MUST be the absolute last part)
        # Aggregate usage if multiple steps were used
        final_usage = {"promptTokens": 50, "completionTokens": 75} # Example, sum up usage from all 'e' parts if applicable
        yield f'd:{json.dumps({"finishReason": "stop", "usage": final_usage})}\n'
        # --- Stream ENDS here ---

    # IMPORTANT: Set the custom header and correct media type
    return StreamingResponse(
        generate_data_stream(),
        media_type="text/plain", # The underlying stream is text
        headers={'X-Vercel-AI-Data-Stream': 'v1'} # Crucial header for the SDK
    )

