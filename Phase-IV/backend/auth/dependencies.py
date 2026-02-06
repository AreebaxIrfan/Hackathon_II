from fastapi import HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from auth.jwt import verify_token
from typing import Dict
import uuid

# Initialize security scheme
oauth2_scheme = HTTPBearer()

async def get_current_user(token: HTTPAuthorizationCredentials = Depends(oauth2_scheme)) -> Dict:
    """
    Dependency to get the current user from the JWT token.
    """
    try:
        payload = verify_token(token.credentials)
        user_id: str = payload.get("sub")

        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )

        # Create user object with extracted info
        user = {
            "user_id": uuid.UUID(user_id),
            "email": payload.get("email"),
            "exp": payload.get("exp")
        }

        return user
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

# Alias for easier import
require_authentication = get_current_user