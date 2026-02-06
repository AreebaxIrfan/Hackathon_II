from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlmodel import Session
from datetime import timedelta
from sqlmodel.ext.asyncio.session import AsyncSession
from src.database import get_session
from src.models.user import User
from src.schemas.user_schemas import UserLogin, Token, UserResponse
from src.models.user import UserCreate as UserCreateSchema
from auth.jwt import create_access_token
from services.user_service import create_user, authenticate_user, get_user_by_email
from core.logging import log_successful_login, log_failed_login, log_registration_success

router = APIRouter()
security = HTTPBearer()

@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(user_data: UserCreateSchema, session: AsyncSession = Depends(get_session)):
    """
    Register a new user.
    """
    # Check if user already exists
    existing_user = await get_user_by_email(session, user_data.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email already exists"
        )

    # Create new user
    try:
        user = await create_user(session, user_data.email, user_data.password)

        # Log registration success
        log_registration_success(str(user.id), user.email)

        # Return success response without exposing sensitive data
        return {
            "id": str(user.id),
            "email": user.email,
            "created_at": user.created_at.isoformat(),
            "is_active": True
        }
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred during registration"
        )

@router.post("/login", response_model=Token)
async def login(user_data: UserLogin, session: AsyncSession = Depends(get_session)):
    """
    Authenticate user and return access token.
    """
    user = await authenticate_user(session, user_data.email, user_data.password)
    if not user:
        # Log failed login
        log_failed_login(user_data.email)

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Create access token
    access_token_expires = timedelta(minutes=15)
    access_token = create_access_token(
        data={"sub": str(user.id), "email": user.email}
    )

    # Log successful login
    log_successful_login(str(user.id))

    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/me")
async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    session: AsyncSession = Depends(get_session)
):
    """
    Get current user information.
    """
    from auth.jwt import verify_token
    import uuid

    token_data = verify_token(credentials.credentials)
    user_id = token_data.get("sub")

    user = await session.get(User, uuid.UUID(user_id))
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    return {
        "id": str(user.id),
        "email": user.email,
        "created_at": user.created_at.isoformat(),
        "is_active": user.is_active
    }