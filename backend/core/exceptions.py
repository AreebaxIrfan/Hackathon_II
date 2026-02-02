from fastapi import HTTPException, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

class AuthException(HTTPException):
    """Custom exception for authentication-related errors."""
    pass

class UserNotFoundException(AuthException):
    """Raised when a user is not found."""
    def __init__(self, email: str):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with email '{email}' not found"
        )

class UserAlreadyExistsException(AuthException):
    """Raised when trying to create a user that already exists."""
    def __init__(self, email: str):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"User with email '{email}' already exists"
        )

class InvalidCredentialsException(AuthException):
    """Raised when login credentials are invalid."""
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Bearer"}
        )

class InsufficientPermissionsException(AuthException):
    """Raised when a user doesn't have sufficient permissions."""
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Insufficient permissions"
        )

async def validation_exception_handler(request, exc: RequestValidationError):
    """Handle validation errors."""
    errors = []
    for error in exc.errors():
        errors.append({
            "loc": error['loc'],
            "msg": error['msg'],
            "type": error['type']
        })

    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"detail": "Validation error", "errors": errors}
    )

async def auth_exception_handler(request, exc: AuthException):
    """Handle authentication exceptions."""
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail}
    )