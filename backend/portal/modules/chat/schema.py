from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel


# ----------------
# MESSAGE
# ----------------
class MessageBase(BaseModel):
    sender: str
    content: str


class MessageCreate(MessageBase):
    conversation_id: int


class MessageRead(MessageBase):
    id: int
    created_at: Optional[datetime] = None

    class Config:
        orm_mode = True


# ----------------
# CONVERSATION
# ----------------
class ConversationCreate(BaseModel):
    title: str


class ConversationRead(BaseModel):
    id: int
    title: str
    created_at: Optional[datetime] = None
    messages: List[MessageRead] = []

    class Config:
        orm_mode = True
