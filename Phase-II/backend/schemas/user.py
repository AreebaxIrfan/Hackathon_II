from pydantic import BaseModel, field_validator
from typing import Optional
from datetime import datetime
import uuid
import re

class UserBase(BaseModel):
    email: str

    @field_validator('email')
    @classmethod
    def validate_email(cls, v):
        if not re.match(r'^[^@]+@[^@]+\.[^@]+$', v):
            raise ValueError('Invalid email format')
        return v.lower()

class UserCreate(UserBase):
    password: str

    @field_validator('password')
    @classmethod
    def validate_password(cls, v):
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters long')
        if not re.search(r'[A-Z]', v):
            raise ValueError('Password must contain at least one uppercase letter')
        if not re.search(r'[a-z]', v):
            raise ValueError('Password must contain at least one lowercase letter')
        if not re.search(r'\d', v):
            raise ValueError('Password must contain at least one digit')
        return v

class UserLogin(BaseModel):
    email: str
    password: str

    @field_validator('email')
    @classmethod
    def validate_email(cls, v):
        if not re.match(r'^[^@]+@[^@]+\.[^@]+$', v):
            raise ValueError('Invalid email format')
        return v.lower()

class UserUpdate(BaseModel):
    email: Optional[str] = None
    is_active: Optional[bool] = None

    @field_validator('email', mode='before')
    @classmethod
    def validate_optional_email(cls, v):
        if v is not None:
            if not re.match(r'^[^@]+@[^@]+\.[^@]+$', v):
                raise ValueError('Invalid email format')
            return v.lower()
        return v

class UserResponse(UserBase):
    id: uuid.UUID
    created_at: datetime
    is_active: bool

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    user_id: uuid.UUID
    email: str