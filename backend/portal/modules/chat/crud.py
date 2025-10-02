"""chat crud helpers"""
from typing import List, Optional

from sqlalchemy.orm import Session, joinedload

from portal.modules.postgres import models
from portal.modules.postgres.crud import CRUDBase

from . import schema


class CRUDConversation(
    CRUDBase[models.Conversation, schema.ConversationCreate, schema.ConversationCreate]
):
    def get_with_messages(self, db: Session, id: int) -> Optional[models.Conversation]:
        """get one conversation with its messages"""
        return (
            db.query(models.Conversation)
            .options(joinedload(models.Conversation.messages))
            .filter(models.Conversation.id == id)
            .first()
        )

    def get_multi(
        self, db: Session, skip: int = 0, limit: int = 100
    ) -> List[models.Conversation]:
        """list conversations without messages (lightweight)"""
        return db.query(models.Conversation).offset(skip).limit(limit).all()


class CRUDMessage(CRUDBase[models.Message, schema.MessageCreate, schema.MessageCreate]):
    def get_by_conversation(
        self, db: Session, conversation_id: int
    ) -> List[models.Message]:
        """get all messages of a conversation"""
        return (
            db.query(models.Message)
            .filter(models.Message.conversation_id == conversation_id)
            .order_by(models.Message.created_at.asc())
            .all()
        )


conversation = CRUDConversation(models.Conversation)
message = CRUDMessage(models.Message)
