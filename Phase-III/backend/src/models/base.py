from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4
from sqlmodel import Field, SQLModel


class TimestampMixin(SQLModel):
    """Mixin class to add timestamp fields to models."""
    created_at: Optional[datetime] = Field(default_factory=datetime.now)
    updated_at: Optional[datetime] = Field(default_factory=datetime.now, nullable=False)


class UUIDModel(SQLModel):
    """Base model with UUID primary key."""
    id: Optional[UUID] = Field(default_factory=uuid4, primary_key=True)