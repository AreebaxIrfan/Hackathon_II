from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime
from uuid import UUID

class UserSchemaBase(BaseModel):
    email: str

class UserLogin(BaseModel):
    email: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    user_id: UUID
    email: str

class UserResponse(BaseModel):
    id: UUID
    email: str
    created_at: datetime
    is_active: bool
