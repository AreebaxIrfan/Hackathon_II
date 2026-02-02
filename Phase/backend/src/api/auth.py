from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from typing import Optional
from datetime import timedelta
from backend.src.db.session import get_session
from backend.src.api.deps import create_access_token, hash_password
from backend.src.models.task import TaskCreate
import os
from dotenv import load_dotenv
from pydantic import BaseModel

load_dotenv()

router = APIRouter()


class UserCreateRequest(BaseModel):
    email: str
    password: str


class UserLoginRequest(BaseModel):
    email: str
    password: str


@router.post("/register")
def register(user_data: UserCreateRequest, session: Session = Depends(get_session)):
    """
    Register a new user account.
    """
    # In a real implementation, we'd create a User model and store the user
    # For now, we'll simulate the registration process
    hashed_password = hash_password(user_data.password)

    # Here we would normally save the user to the database
    # For now, we'll just return a success message

    # Create access token for the new user (using email as identifier for demo)
    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(
        data={"sub": user_data.email}, expires_delta=access_token_expires
    )

    return {
        "message": "User registered successfully",
        "access_token": access_token,
        "token_type": "bearer",
        "user": {"email": user_data.email}
    }


@router.post("/login")
def login(user_data: UserLoginRequest, session: Session = Depends(get_session)):
    """
    Authenticate user and return JWT token.
    """
    # In a real implementation, we'd look up the user in the database
    # For now, we'll just verify the password against a hardcoded user
    # This is just a simulation - in a real app, we'd have a User model

    # For demo purposes, accept any email/password combination
    # In reality, you'd check against stored user data
    if not user_data.email or not user_data.password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Create access token
    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(
        data={"sub": user_data.email}, expires_delta=access_token_expires
    )

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": {"email": user_data.email}
    }


@router.post("/logout")
def logout():
    """
    Logout user and invalidate session.
    """
    # In a real implementation, we might add the token to a blacklist
    # For now, we just confirm the logout
    return {"message": "Successfully logged out"}