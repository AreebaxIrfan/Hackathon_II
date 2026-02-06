from datetime import datetime
from typing import Optional, List
from uuid import UUID
from sqlmodel import Field, SQLModel, Relationship
from .base import UUIDModel, TimestampMixin


class ConversationBase(SQLModel):
    title: Optional[str] = Field(default=None)


class Conversation(UUIDModel, ConversationBase, TimestampMixin, table=True):
    __tablename__ = "conversations"

    user_id: UUID = Field(foreign_key="users.id", nullable=False)

    # Relationships
    user: "User" = Relationship(back_populates="conversations")
    messages: List["Message"] = Relationship(back_populates="conversation")
    tool_calls: List["ToolCall"] = Relationship(back_populates="conversation")


class ConversationCreate(ConversationBase):
    user_id: UUID


class ConversationRead(ConversationBase):
    id: UUID
    user_id: UUID
    created_at: datetime
    updated_at: datetime


class ConversationUpdate(SQLModel):
    title: Optional[str] = None