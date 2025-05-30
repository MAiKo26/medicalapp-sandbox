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
        # Simulate processing time / streaming delay
        delay = 0.05 # Reduced delay for faster example

        print("Starting data stream...")

        # Each yield must be a complete SSE 'data:' line followed by two newlines
        # The Vercel AI SDK expects a *JSON string* as the data payload, not just a string,
        # which it then decodes and processes based on the prefix.

        # Corrected: Type prefix (e.g., '0:') is *inside* the JSON string
        # and the JSON string is the *value* of the data: field.
        # So the format is data:JSON_STRING_OF_PAYLOAD\n\n
        # The payload itself is then like {"type": "text", "text": "..."}

        # 0: Text Part (UIMessageStreamPart of type 'text')
        # The value associated with 'text' is the text content itself (string)
        # Note: The '0:' prefix in your previous example was part of a custom protocol,
        # but the AI SDK expects a 'type' field within the JSON for standard parts.
        # If your client-side `index.js` specifically uses `type: "text"` from the JSON,
        # then you should send a JSON object like `{"type": "text", "text": "..."}`
        # The client-side `uiMessageStreamPartSchema` and `processUIMessageStream`
        # in `index.js` confirm the expectation of `{"type": "text", "text": "..."}`.
        yield f'data:{json.dumps({"type": "text", "text": "Hello! This is the initial text. ","id":"0"})}\n\n'
        await asyncio.sleep(delay)
        yield f'data:{json.dumps({"type": "text", "text": "Here is some more text.", "id":"1"})}\n\n'
        await asyncio.sleep(delay)

        # f: Start Step Part (type: "start-step")
        yield f'data:{json.dumps({"type": "start-step", "messageId": "step-1"})}\n\n'
        await asyncio.sleep(delay)

        # g: Reasoning Part (type: "reasoning")
        yield f'data:{json.dumps({"type": "reasoning", "text": "Okay"})}\n\n'
        await asyncio.sleep(delay)
        yield f'data:{json.dumps({"type": "reasoning", "text": "planning"})}\n\n'
        await asyncio.sleep(delay)
        yield f'data:{json.dumps({"type": "reasoning", "text": "the"})}\n\n'
        await asyncio.sleep(delay)
        yield f'data:{json.dumps({"type": "reasoning", "text": "first"})}\n\n'
        await asyncio.sleep(delay)
        yield f'data:{json.dumps({"type": "reasoning", "text": "step..."})}\n\n'
        await asyncio.sleep(delay)
        yield f'data:{json.dumps({"type": "reasoning", "text": " I will now search for relevant information."})}\n\n'
        await asyncio.sleep(delay)

        yield f'data:{json.dumps({"type": "text", "text": "Here is 2 some more text.","id":"ABC"})}\n\n'
        await asyncio.sleep(delay)


        # 8: Message Annotation Part (type: "message-annotation")
        yield f'data:{json.dumps({"type": "data-annotation", "data": [{"type": "citation", "id": "anno-1", "text": "Source [1]", "details": {"sourceId": "src-1"}}]})}\n\n'
        yield f'data:{json.dumps({"type": "data-annotation", "data": [{"type": "citation", "id": "anno-2", "text": "Another Source [2]", "details": {"sourceId": "src-2"}}]})}\n\n'
        await asyncio.sleep(delay)

        # i: Redacted Reasoning Part (type: "redacted-reasoning")
        yield f'data:{json.dumps({"type": "redacted-reasoning", "redactedtext": "[REDACTED: Potentially sensitive internal thought process]"})}\n\n'
        await asyncio.sleep(delay)

        # j: Reasoning Signature Part (type: "reasoning-signature")
        yield f'data:{json.dumps({"type": "reasoning-signature", "signature": "sig_aBcDeF12345"})}\n\n'
        await asyncio.sleep(delay)



        # h: Source Part (type: "source")
        yield f'data:{json.dumps({"type": "source", "id": "src-1", "sourceType": "url", "url": "https://vercel.com/docs", "title": "Vercel Documentation"})}\n\n'
        await asyncio.sleep(delay)
        yield f'data:{json.dumps({"type": "source", "id": "src-2", "sourceType": "text", "content": "Internal knowledge base article #42"})}\n\n'
        await asyncio.sleep(delay)

        # k: File Part (type: "file-part")
        file_content = "This is the content of the file."
        file_data_base64 = base64.b64encode(file_content.encode('utf-8')).decode('utf-8')
        yield f'data:{json.dumps({"type": "file-part", "data": file_data_base64, "mimeType": "text/plain;charset=utf-8"})}\n\n'
        await asyncio.sleep(delay)

        # 2: Data Part (type: "data") - Arbitrary JSON data
        yield f'data:{json.dumps({"type": "data", "data": [{"status": "Searching..."}, {"query": 1}]})}\n\n'
        await asyncio.sleep(delay)
        yield f'data:{json.dumps({"type": "data", "data": [{"results_found": 5}]})}\n\n'
        await asyncio.sleep(delay)

        # 3: Error Part (type: "error")
        yield f'data:{json.dumps({"type": "error", "errorText": "Encountered a minor issue during search, but continuing."})}\n\n'
        await asyncio.sleep(delay)

        # ---- Tool Call Example (Streaming) ----
        tool_call_id_stream = "call_stream_weather_123"
        tool_name_stream = "get_current_weather_streaming"
        # b: Tool Call Streaming Start Part (type: "tool-call-streaming-start")
        yield f'data:{json.dumps({"type": "tool-call-streaming-start", "toolCallId": tool_call_id_stream, "toolName": tool_name_stream})}\n\n'
        await asyncio.sleep(delay)
        # c: Tool Call Delta Part(s) (type: "tool-call-delta")
        yield f'data:{json.dumps({"type": "tool-call-delta", "toolCallId": tool_call_id_stream, "argsTextDelta": '{"loc'})}\n\n'
        await asyncio.sleep(0.1)
        yield f'data:{json.dumps({"type": "tool-call-delta", "toolCallId": tool_call_id_stream, "argsTextDelta": 'ation"'})}\n\n'
        await asyncio.sleep(0.1)
        yield f'data:{json.dumps({"type": "tool-call-delta", "toolCallId": tool_call_id_stream, "argsTextDelta": ': "Tun'})}\n\n'
        await asyncio.sleep(0.1)
        yield f'data:{json.dumps({"type": "tool-call-delta", "toolCallId": tool_call_id_stream, "argsTextDelta": 'is, '})}\n\n'
        await asyncio.sleep(0.1)
        yield f'data:{json.dumps({"type": "tool-call-delta", "toolCallId": tool_call_id_stream, "argsTextDelta": 'TN"}'})}\n\n'
        await asyncio.sleep(delay)
        # 9: Tool Call Part (type: "tool-call") - Needs to come *after* streaming deltas for the same call
        yield f'data:{json.dumps({"type": "tool-call", "toolCallId": tool_call_id_stream, "toolName": tool_name_stream, "args": {"location": "Tunis, TN"}})}\n\n'
        await asyncio.sleep(delay)
        # a: Tool Result Part (type: "tool-result")
        yield f'data:{json.dumps({"type": "tool-result", "toolCallId": tool_call_id_stream, "result": {"temperature": "25C", "condition": "Sunny"}})}\n\n'
        await asyncio.sleep(delay)
        # ---- End Tool Call Example (Streaming) ----

        # ---- Tool Call Example (Non-Streaming) ----
        tool_call_id_nonstream = "call_nonstream_user_456"
        tool_name_nonstream = "lookup_user_info"
        # 9: Tool Call Part (type: "tool-call") - Sent directly
        yield f'data:{json.dumps({"type": "tool-call", "toolCallId": tool_call_id_nonstream, "toolName": tool_name_nonstream, "args": {"user_id": "usr_abc"}})}\n\n'
        await asyncio.sleep(delay)
        # a: Tool Result Part (type: "tool-result")
        yield f'data:{json.dumps({"type": "tool-result", "toolCallId": tool_call_id_nonstream, "result": {"name": "John Doe", "status": "Active"}})}\n\n'
        await asyncio.sleep(delay)
        # ---- End Tool Call Example (Non-Streaming) ----

        # e: Finish Step Part (type: "finish-step")
        yield f'data:{json.dumps({"type": "finish-step", "finishReason": "tool-calls", "usage": {"promptTokens": 50, "completionTokens": 75}, "isContinued": False})}\n\n'
        await asyncio.sleep(delay)

        # Optionally start another step if needed
        # yield f'data:{json.dumps({"type": "start-step", "messageId": "step-2"})}\n\n'
        # ... more parts ...
        # yield f'data:{json.dumps({"type": "finish-step", "finishReason": "stop", "usage": {"promptTokens": 10, "completionTokens": 20}, "isContinued": False})}\n\n'

        # d: Finish Message Part (type: "finish-message") - MUST be the absolute last part
        final_usage = {"promptTokens": 50, "completionTokens": 75} # Example, sum up usage from all 'e' parts if applicable
        yield f'data:{json.dumps({"type": "finish-message", "finishReason": "stop", "usage": final_usage})}\n\n'
        # --- Stream ENDS here ---

    return StreamingResponse(
        generate_data_stream(),
        media_type="text/event-stream", # CRUCIAL: Set to text/event-stream
        headers={
            'X-Vercel-AI-Data-Stream': 'v1', # CRUCIAL: Header for the SDK
            'Cache-Control': 'no-cache',     # Recommended for SSE
            'Connection': 'keep-alive'       # Recommended for SSE
        }
    )