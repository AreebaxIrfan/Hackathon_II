from datetime import datetime
from typing import Optional, List
from uuid import UUID
from sqlmodel import Field, SQLModel, Relationship
from .base import UUIDModel, TimestampMixin


class UserBase(SQLModel):
    email: str = Field(unique=True, index=True)
    username: Optional[str] = Field(default=None, unique=True, index=True)
    is_active: bool = Field(default=True)


class User(UUIDModel, UserBase, TimestampMixin, table=True):
    __tablename__ = "users"

    hashed_password: str = Field(nullable=False)

    # Relationships
    todos: List["Todo"] = Relationship(back_populates="user")
    conversations: List["Conversation"] = Relationship(back_populates="user")


class UserCreate(UserBase):
    password: str


class UserRead(UserBase):
    id: UUID
    created_at: datetime
    updated_at: datetime


class UserUpdate(SQLModel):
    email: Optional[str] = None
    username: Optional[str] = None
    password: Optional[str] = None
    is_active: Optional[bool] = None