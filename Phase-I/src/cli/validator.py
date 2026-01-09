"""Input validation functions for CLI layer.

This module provides reusable validation functions for user input
including title and ID validation with clear error messages.
"""


def validate_title(title: str) -> None:
    """Validate that title is non-empty and not whitespace-only.

    Args:
        title: The title string to validate

    Raises:
        ValueError: If title is empty or whitespace-only
    """
    if not title or not title.strip():
        raise ValueError("Title cannot be empty")


def validate_id(todo_id: str) -> int:
    """Validate and convert ID string to positive integer.

    Args:
        todo_id: The ID string to validate

    Returns:
        int: Validated positive integer ID

    Raises:
        ValueError: If ID is not a positive integer
    """
    try:
        id_int = int(todo_id)
        if id_int <= 0:
            raise ValueError("ID must be a positive integer")
        return id_int
    except ValueError as e:
        if "positive integer" in str(e):
            raise
        raise ValueError("ID must be a valid integer")
