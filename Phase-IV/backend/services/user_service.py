from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select
from src.models.user import User
from auth.jwt import get_password_hash
from typing import Optional
import uuid

async def create_user(session: AsyncSession, email: str, password: str) -> User:
    """
    Create a new user with hashed password.
    """
    # Hash the password
    hashed_password = get_password_hash(password)
    # Create user instance
    user = User(
        email=email,
        hashed_password=hashed_password
    )

    # Add to session and commit
    session.add(user)
    await session.commit()
    await session.refresh(user)

    return user

async def get_user_by_email(session: AsyncSession, email: str) -> Optional[User]:
    """
    Get a user by email.
    """
    statement = select(User).where(User.email == email)
    result = await session.exec(statement)
    user = result.first()
    return user

async def get_user_by_id(session: AsyncSession, user_id: uuid.UUID) -> Optional[User]:
    """
    Get a user by ID.
    """
    statement = select(User).where(User.id == user_id)
    result = await session.exec(statement)
    user = result.first()
    return user

async def authenticate_user(session: AsyncSession, email: str, password: str) -> Optional[User]:
    """
    Authenticate a user by email and password.
    """
    from auth.jwt import verify_password

    # Find user by email
    user = await get_user_by_email(session, email)

    if not user or not verify_password(password, user.hashed_password):
        return None

    return user