from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import Optional


class ConversationBase(SQLModel):
    user_id: str = Field(foreign_key="user.id")


class Conversation(ConversationBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: str = Field(foreign_key="user.id")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class ConversationCreate(ConversationBase):
    pass


class ConversationUpdate(SQLModel):
    pass


class ConversationRead(ConversationBase):
    id: int
    created_at: datetime
    updated_at: datetime