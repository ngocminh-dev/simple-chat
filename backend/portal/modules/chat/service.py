import os
from typing import AsyncGenerator

import httpx
from sqlalchemy.orm import Session

from portal.modules.postgres import models

LMSTUDIO_URL = f"{os.getenv('LMSTUDIO_API')}/v1/chat/completions"


def generate_ai_response(prompt: str) -> str:
    payload = {
        "model": "local-model",  # adjust to your model
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.7,
    }
    try:
        response = httpx.post(LMSTUDIO_URL, json=payload, timeout=60)
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"]
    except Exception as e:
        return f"(AI Error: {e})"


async def stream_ai_response(prompt: str) -> AsyncGenerator[str, None]:
    """stream response tokens from local AI model"""
    payload = {
        "model": "local-model",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.7,
        "stream": True,
    }

    async with httpx.AsyncClient(timeout=None) as client:
        async with client.stream("POST", LMSTUDIO_URL, json=payload) as response:
            async for line in response.aiter_lines():
                if not line or not line.startswith("data: "):
                    continue
                data = line.removeprefix("data: ").strip()
                if data == "[DONE]":
                    break
                try:
                    token = (
                        httpx.Response(200, content=data)
                        .json()["choices"][0]["delta"]
                        .get("content")
                    )
                    if token:
                        yield token
                except Exception:
                    continue


def save_message(
    db: Session, conversation_id: int, sender: str, content: str
) -> models.Message:
    msg = models.Message(
        conversation_id=conversation_id, sender=sender, content=content
    )
    db.add(msg)
    db.commit()
    db.refresh(msg)
    return msg
