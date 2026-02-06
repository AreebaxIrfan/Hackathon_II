from datetime import datetime
from typing import Optional, List
from uuid import UUID
from sqlmodel import Field, SQLModel, Relationship
from .base import UUIDModel, TimestampMixin


class TodoBase(SQLModel):
    title: str = Field(min_length=1, max_length=200)
    description: Optional[str] = Field(default=None)
    completed: bool = Field(default=False)
    priority: Optional[int] = Field(default=1, ge=1, le=5)
    due_date: Optional[datetime] = Field(default=None)


class Todo(UUIDModel, TodoBase, TimestampMixin, table=True):
    __tablename__ = "todos"

    user_id: UUID = Field(foreign_key="users.id", nullable=False)

    # Relationship
    user: "User" = Relationship(back_populates="todos")


class TodoCreate(TodoBase):
    pass


class TodoRead(TodoBase):
    id: UUID
    user_id: UUID
    completed: bool
    priority: Optional[int]
    due_date: Optional[datetime]
    created_at: datetime
    updated_at: datetime


class TodoUpdate(SQLModel):
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None
    priority: Optional[int] = Field(default=None, ge=1, le=5)
    due_date: Optional[datetime] = None