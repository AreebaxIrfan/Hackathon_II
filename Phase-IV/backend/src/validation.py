"""
Validation utilities for the Chat Flow API
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


def validate_message_content(content: str) -> bool:
    """
    Validate the message content.

    Args:
        content: The message content to validate

    Returns:
        True if valid, raises HTTPException if invalid
    """
    if not content or not isinstance(content, str):
        raise HTTPException(
            status_code=400,
            detail="Message content is required and must be a string"
        )

    if len(content) < 1 or len(content) > 5000:
        raise HTTPException(
            status_code=400,
            detail="Message content must be between 1 and 5000 characters"
        )

    return True


def validate_conversation_id(conv_id: Optional[str]) -> bool:
    """
    Validate the conversation ID format.

    Args:
        conv_id: The conversation ID to validate (can be None)

    Returns:
        True if valid, raises HTTPException if invalid
    """
    if conv_id is not None:
        if not isinstance(conv_id, str):
            raise HTTPException(
                status_code=400,
                detail="Conversation ID must be a string if provided"
            )

        # Basic validation - alphanumeric, underscore, hyphen, 1-64 chars
        if not re.match(r'^[a-zA-Z0-9_-]{1,64}$', conv_id):
            raise HTTPException(
                status_code=400,
                detail="Conversation ID must be 1-64 characters and contain only letters, numbers, underscores, or hyphens"
            )

    return True


def validate_role(role: str) -> bool:
    """
    Validate the message role.

    Args:
        role: The role to validate

    Returns:
        True if valid, raises HTTPException if invalid
    """
    if role not in ["user", "assistant"]:
        raise HTTPException(
            status_code=400,
            detail="Role must be either 'user' or 'assistant'"
        )

    return True


def validate_tool_call(tool_name: str) -> bool:
    """
    Validate the tool call name.

    Args:
        tool_name: The tool name to validate

    Returns:
        True if valid, raises HTTPException if invalid
    """
    if not tool_name or not isinstance(tool_name, str):
        raise HTTPException(
            status_code=400,
            detail="Tool name is required and must be a string"
        )

    # Allow alphanumeric, hyphens, and underscores
    if not re.match(r'^[a-zA-Z0-9_-]+$', tool_name):
        raise HTTPException(
            status_code=400,
            detail="Tool name must contain only letters, numbers, hyphens, or underscores"
        )

    return True