from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List, Dict, Any
from datetime import datetime
from uuid import UUID
from .base import UUIDModel, TimestampMixin

class ToolCallBase(SQLModel):
    conversation_id: UUID = Field(foreign_key="conversations.id")
    tool_name: str = Field(max_length=100)
    arguments: str  # JSON string
    result: Optional[str] = None  # JSON string


class ToolCall(UUIDModel, ToolCallBase, TimestampMixin, table=True):
    __tablename__ = "tool_calls"

    # Relationships
    conversation: "Conversation" = Relationship(back_populates="tool_calls")


class ToolCallCreate(ToolCallBase):
    pass


class ToolCallUpdate(SQLModel):
    result: Optional[str] = None  # JSON string


class ToolCallRead(ToolCallBase):
    id: UUID
    created_at: datetime