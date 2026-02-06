from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from datetime import datetime
from uuid import UUID
from .base import UUIDModel, TimestampMixin

class MessageBase(SQLModel):
    user_id: UUID = Field(foreign_key="users.id")
    conversation_id: UUID = Field(foreign_key="conversations.id")
    role: str = Field(regex="^(user|assistant)$")
    content: str = Field(min_length=1, max_length=5000)


class Message(UUIDModel, MessageBase, TimestampMixin, table=True):
    __tablename__ = "messages"

    # Relationships
    conversation: "Conversation" = Relationship(back_populates="messages")


class MessageCreate(MessageBase):
    pass


class MessageUpdate(SQLModel):
    content: Optional[str] = Field(default=None, min_length=1, max_length=5000)


class MessageRead(MessageBase):
    id: UUID
    created_at: datetime