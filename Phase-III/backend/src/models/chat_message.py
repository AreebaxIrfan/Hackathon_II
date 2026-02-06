from datetime import datetime
from typing import Optional
from uuid import UUID
from sqlmodel import Field, SQLModel, Relationship
from sqlalchemy import Column, String
from .base import UUIDModel, TimestampMixin


class ChatMessageBase(SQLModel):
    conversation_id: UUID = Field(foreign_key="conversations.id", nullable=False)
    sender_type: str = Field(sa_column=Column(String, nullable=False))
    content: str = Field(min_length=1)
    metadata: Optional[dict] = Field(default=None)


class ChatMessage(UUIDModel, ChatMessageBase, TimestampMixin, table=True):
    __tablename__ = "chat_messages"

    timestamp: datetime = Field(default_factory=datetime.now)

    # Relationships
    conversation: "Conversation" = Relationship(back_populates="messages")


class ChatMessageCreate(ChatMessageBase):
    pass


class ChatMessageRead(ChatMessageBase):
    id: UUID
    timestamp: datetime


class ChatMessageUpdate(SQLModel):
    content: Optional[str] = None
    metadata: Optional[dict] = None