from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import Optional


class MessageBase(SQLModel):
    user_id: str = Field(foreign_key="user.id")
    conversation_id: int = Field(foreign_key="conversation.id")
    role: str = Field(regex="^(user|assistant)$")
    content: str = Field(min_length=1, max_length=5000)


class Message(MessageBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: str = Field(foreign_key="user.id")
    conversation_id: int = Field(foreign_key="conversation.id")
    role: str = Field(regex="^(user|assistant)$")
    content: str = Field(min_length=1, max_length=5000)
    created_at: datetime = Field(default_factory=datetime.utcnow)


class MessageCreate(MessageBase):
    pass


class MessageUpdate(SQLModel):
    content: Optional[str] = Field(default=None, min_length=1, max_length=5000)


class MessageRead(MessageBase):
    id: int
    created_at: datetime