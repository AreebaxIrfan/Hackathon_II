from fastapi import APIRouter, Depends
from auth.dependencies import get_current_user
from typing import Dict

router = APIRouter()

@router.get("/profile")
async def get_profile(current_user: Dict = Depends(get_current_user)):
    """
    Example of a protected endpoint that requires authentication.
    Returns the current user's information.
    """
    return {
        "message": "Successfully accessed protected resource",
        "user": {
            "id": str(current_user["user_id"]),
            "email": current_user["email"]
        }
    }

@router.get("/dashboard")
async def get_dashboard(current_user: Dict = Depends(get_current_user)):
    """
    Another example of a protected endpoint.
    """
    return {
        "message": "Welcome to your dashboard",
        "user_id": str(current_user["user_id"]),
        "timestamp": "Just accessed"
    }