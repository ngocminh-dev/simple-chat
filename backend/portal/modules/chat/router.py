import json

from fastapi import APIRouter, Depends, HTTPException, WebSocket, WebSocketDisconnect

from portal.modules.postgres.database import DB

from . import crud, schema, service

router = APIRouter(prefix="/chat", tags=["Chat"])

# -----------------
# REST CRUD ROUTES
# -----------------


@router.post("/conversations", response_model=schema.ConversationRead)
def create_conversation(convo: schema.ConversationCreate, db: DB):
    return crud.conversation.create(db, obj_in=convo)


@router.get("/conversations", response_model=list[schema.ConversationRead])
def list_conversations(db: DB, skip: int = 0, limit: int = 100):
    return crud.conversation.get_multi(db, skip=skip, limit=limit)


@router.get("/conversations/{conversation_id}", response_model=schema.ConversationRead)
def get_conversation(conversation_id: int, db: DB):
    convo = crud.conversation.get_with_messages(db, id=conversation_id)
    if not convo:
        raise HTTPException(status_code=404, detail="Conversation not found")
    return convo


@router.delete("/conversations/{conversation_id}")
def delete_conversation(conversation_id: int, db: DB):
    deleted = crud.conversation.remove(db, id=conversation_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Conversation not found")
    return {"status": "deleted"}


@router.get(
    "/conversations/{conversation_id}/messages", response_model=list[schema.MessageRead]
)
def list_messages(conversation_id: int, db: DB):
    return crud.message.get_by_conversation(db, conversation_id)


# -----------------
# WebSocket STREAM
# -----------------


@router.websocket("/ws/{conversation_id}")
async def chat_ws(websocket: WebSocket, conversation_id: int, db: DB):
    await websocket.accept()

    convo = crud.conversation.get(db, id=conversation_id)
    if not convo:
        await websocket.send_json({"error": "Conversation not found"})
        await websocket.close()
        return

    try:
        while True:
            data = await websocket.receive_text()
            msg_data = json.loads(data)

            # Save user message
            user_msg = crud.message.create(
                db,
                obj_in=schema.MessageCreate(
                    sender="user",
                    content=msg_data["content"],
                    conversation_id=conversation_id,
                ),
            )

            await websocket.send_json(
                {
                    "sender": "user",
                    "content": user_msg.content,
                    "id": user_msg.id,
                    "partial": False,
                }
            )

            # Stream AI response
            collected = ""
            async for token in service.stream_ai_response(msg_data["content"]):
                collected += token
                await websocket.send_json(
                    {
                        "sender": "assistant",
                        "content": token,
                        "partial": True,
                    }
                )

            # Save final AI message
            ai_msg = crud.message.create(
                db,
                obj_in=schema.MessageCreate(
                    sender="assistant",
                    content=collected,
                    conversation_id=conversation_id,
                ),
            )

            await websocket.send_json(
                {
                    "sender": "assistant",
                    "content": ai_msg.content,
                    "id": ai_msg.id,
                    "partial": False,
                }
            )

    except WebSocketDisconnect:
        print(f"Disconnected from conversation {conversation_id}")
