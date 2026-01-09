"""
Todo data model for Phase I Todo In-Memory Console App.

This module defines the Todo entity using Python dataclass for type safety,
clean code, and minimal boilerplate.
"""

from dataclasses import dataclass


@dataclass
class Todo:
    """Represents a single todo item.

    Attributes:
        id (int): Unique numeric identifier
        title (str): Required title for the todo
        description (str, optional): Additional details, defaults to empty string
        is_complete (bool): Completion status, defaults to False (incomplete)
    """
    id: int
    title: str
    description: str = ""
    is_complete: bool = False
