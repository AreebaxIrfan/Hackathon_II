from sqlmodel import Session, select
from models.user import User
from auth.jwt import get_password_hash
from typing import Optional
import uuid

def create_user(session: Session, email: str, password: str) -> User:
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
    session.commit()
    session.refresh(user)

    return user

def get_user_by_email(session: Session, email: str) -> Optional[User]:
    """
    Get a user by email.
    """
    statement = select(User).where(User.email == email)
    user = session.exec(statement).first()
    return user

def get_user_by_id(session: Session, user_id: uuid.UUID) -> Optional[User]:
    """
    Get a user by ID.
    """
    statement = select(User).where(User.id == user_id)
    user = session.exec(statement).first()
    return user

def authenticate_user(session: Session, email: str, password: str) -> Optional[User]:
    """
    Authenticate a user by email and password.
    """
    from auth.jwt import verify_password

    # Find user by email
    user = get_user_by_email(session, email)

    if not user or not verify_password(password, user.hashed_password):
        return None

    return user