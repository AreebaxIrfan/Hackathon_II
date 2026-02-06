"""
Validation utilities for the MCP Tools
"""
from typing import Dict, Any, Optional
from fastapi import HTTPException
import re


def validate_user_id(user_id: str) -> bool:
    """
    Validate the user ID format.

    Args:
        user_id: The user ID to validate

    Returns:
        True if valid, raises HTTPException if invalid
    """
    if not user_id or not isinstance(user_id, str):
        raise HTTPException(
            status_code=400,
            detail="User ID is required and must be a string"
        )

    # Basic validation - alphanumeric, underscore, hyphen, 1-64 chars
    if not re.match(r'^[a-zA-Z0-9_-]{1,64}$', user_id):
        raise HTTPException(
            status_code=400,
            detail="User ID must be 1-64 characters and contain only letters, numbers, underscores, or hyphens"
        )

    return True


def validate_task_title(title: str) -> bool:
    """
    Validate the task title.

    Args:
        title: The task title to validate

    Returns:
        True if valid, raises HTTPException if invalid
    """
    if not title or not isinstance(title, str):
        raise HTTPException(
            status_code=400,
            detail="Task title is required and must be a string"
        )

    if len(title) < 1 or len(title) > 255:
        raise HTTPException(
            status_code=400,
            detail="Task title must be between 1 and 255 characters"
        )

    return True


def validate_task_description(description: Optional[str]) -> bool:
    """
    Validate the task description.

    Args:
        description: The task description to validate (can be None)

    Returns:
        True if valid, raises HTTPException if invalid
    """
    if description is not None:
        if not isinstance(description, str):
            raise HTTPException(
                status_code=400,
                detail="Task description must be a string if provided"
            )

        if len(description) > 1000:
            raise HTTPException(
                status_code=400,
                detail="Task description must not exceed 1000 characters"
            )

    return True


def validate_task_status(status: Optional[str]) -> bool:
    """
    Validate the task status filter.

    Args:
        status: The status to validate (can be None)

    Returns:
        True if valid, raises HTTPException if invalid
    """
    if status is not None:
        if status not in ["all", "pending", "completed"]:
            raise HTTPException(
                status_code=400,
                detail="Status must be 'all', 'pending', or 'completed' if provided"
            )

    return True