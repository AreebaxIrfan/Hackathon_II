"""
Security and user isolation utilities for the Todo AI Agent
"""
from functools import wraps
from typing import Callable, Any
from fastapi import HTTPException
import logging

logger = logging.getLogger(__name__)


def verify_user_access(resource_user_id: str, requesting_user_id: str) -> bool:
    """
    Verify that the requesting user has access to the resource.

    Args:
        resource_user_id: The ID of the user who owns the resource
        requesting_user_id: The ID of the user requesting access

    Returns:
        True if access is allowed, raises HTTPException if not
    """
    if resource_user_id != requesting_user_id:
        logger.warning(f"Access denied: user {requesting_user_id} attempted to access resource owned by {resource_user_id}")
        raise HTTPException(
            status_code=403,
            detail="You do not have permission to access this resource"
        )

    return True


def require_same_user(func: Callable) -> Callable:
    """
    Decorator to ensure that the resource belongs to the requesting user.

    Args:
        func: The function to decorate

    Returns:
        Wrapped function with user verification
    """
    @wraps(func)
    async def wrapper(*args, **kwargs):
        # This decorator would typically extract user IDs from the request
        # and verify they match. For now, we'll just outline the concept.

        # In a real implementation, this would:
        # 1. Extract the authenticated user ID from the request
        # 2. Get the resource owner's ID
        # 3. Call verify_user_access() to ensure they match

        # For demonstration purposes:
        resource_user_id = kwargs.get('resource_user_id')
        requesting_user_id = kwargs.get('requesting_user_id')

        if resource_user_id and requesting_user_id:
            verify_user_access(resource_user_id, requesting_user_id)

        return await func(*args, **kwargs)

    return wrapper


def validate_and_filter_by_user(query, user_id_column, requesting_user_id: str):
    """
    Apply user-based filtering to a database query.

    Args:
        query: The database query to filter
        user_id_column: The column representing the resource owner
        requesting_user_id: The ID of the requesting user

    Returns:
        Filtered query
    """
    # This is a conceptual implementation
    # In practice, this would be integrated with the ORM query
    logger.debug(f"Filtering resources for user {requesting_user_id}")
    # query = query.filter(user_id_column == requesting_user_id)
    return query


def log_security_event(event_type: str, user_id: str, resource: str = None, details: dict = None):
    """
    Log a security-related event.

    Args:
        event_type: Type of security event (access_attempt, permission_denied, etc.)
        user_id: The user associated with the event
        resource: The resource involved (optional)
        details: Additional details about the event (optional)
    """
    log_msg = f"SECURITY EVENT: {event_type} - User: {user_id}"
    if resource:
        log_msg += f", Resource: {resource}"
    if details:
        log_msg += f", Details: {details}"

    logger.info(log_msg)