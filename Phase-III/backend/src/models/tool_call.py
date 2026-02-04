from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import Optional, Dict, Any
import json


class ToolCallBase(SQLModel):
    conversation_id: int = Field(foreign_key="conversation.id")
    tool_name: str = Field(max_length=100)
    arguments: str  # JSON string
    result: Optional[str] = None  # JSON string


class ToolCall(ToolCallBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    conversation_id: int = Field(foreign_key="conversation.id")
    tool_name: str = Field(max_length=100)
    arguments: str  # JSON string
    result: Optional[str] = None  # JSON string
    created_at: datetime = Field(default_factory=datetime.utcnow)


class ToolCallCreate(ToolCallBase):
    pass


class ToolCallUpdate(SQLModel):
    result: Optional[str] = None  # JSON string


class ToolCallRead(ToolCallBase):
    id: int
    created_at: datetime