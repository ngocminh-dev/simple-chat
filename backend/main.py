# main.py
import os
import json
import httpx
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import JSONResponse

app = FastAPI()

LM_STUDIO_API = os.getenv(
    "LM_STUDIO_API", "http://host.docker.internal:1234/v1/chat/completions")
MODEL_NAME = os.getenv("MODEL_NAME", "openai/gpt-oss-20b")
SYSTEM_PROMPT = "You are a helpful assistant."

# ---------------- REST endpoint----------------


@app.post("/chat")
async def chat_endpoint(payload: dict):
    user_msg = payload.get("message", "")
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": user_msg},
    ]
    async with httpx.AsyncClient(timeout=None) as client:
        resp = await client.post(LM_STUDIO_API, json={
            "model": MODEL_NAME,
            "messages": messages,
            "temperature": 0.7
        })
        data = resp.json()
        reply = data["choices"][0]["message"]["content"]
    return JSONResponse({"reply": reply})

# ---------------- WebSocket endpoint (streaming) ----------------


@app.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: str):
    await websocket.accept()
    try:
        while True:
            raw = await websocket.receive_text()
            obj = json.loads(raw)

            if obj.get("type") != "message":
                await websocket.send_text(json.dumps({"type": "error", "error": "only 'message' supported"}))
                continue

            user_msg = obj.get("message", "")
            messages = [
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_msg},
            ]

            async with httpx.AsyncClient(timeout=None) as client:
                async with client.stream(
                    "POST",
                    LM_STUDIO_API,
                    json={"model": MODEL_NAME,
                          "messages": messages,
                          "temperature": 0.7,
                          "stream": True}
                ) as resp:
                    async for line in resp.aiter_lines():
                        if not line or not line.startswith("data: "):
                            continue
                        data = line[len("data: "):]
                        if data.strip() == "[DONE]":
                            break
                        try:
                            chunk = json.loads(data)
                            delta = chunk["choices"][0]["delta"].get("content")
                            if delta:
                                await websocket.send_text(json.dumps({"type": "partial", "delta": delta}))
                        except Exception as e:
                            await websocket.send_text(json.dumps({"type": "error", "error": str(e)}))

            await websocket.send_text(json.dumps({"type": "end"}))

    except WebSocketDisconnect:
        print(f"client {client_id} disconnected")
