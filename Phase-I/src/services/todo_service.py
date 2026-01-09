"""TodoService - Business logic layer for todo CRUD operations.

This module encapsulates all business logic for creating, reading, updating,
deleting, and toggling todos. Enforces validation rules and maintains
in-memory state with clean separation from CLI layer.
"""

from typing import List, Optional
from src.models.todo import Todo


class NotFoundError(Exception):
    """Exception raised when a todo with specified ID does not exist."""

    def __init__(self, todo_id: int):
        self.todo_id = todo_id
        super().__init__(f"Todo with ID {todo_id} not found")


class TodoService:
    """Service class for managing todo CRUD operations.

    Attributes:
        _todos: In-memory list of Todo objects
        _next_id: Counter for assigning unique IDs
    """

    def __init__(self):
        """Initialize TodoService with empty in-memory storage."""
        self._todos: List[Todo] = []
        self._next_id: int = 1

    def create_todo(self, title: str, description: str = "") -> Todo:
        """Create a new todo item.

        Args:
            title: Required title for the todo
            description: Optional description, defaults to empty string

        Returns:
            Todo: Created todo with assigned ID

        Raises:
            ValueError: If title is empty or whitespace-only
        """
        if not title or not title.strip():
            raise ValueError("Title cannot be empty")

        todo = Todo(
            id=self._next_id,
            title=title.strip(),
            description=description.strip() if description else "",
            is_complete=False
        )
        self._todos.append(todo)
        self._next_id += 1
        return todo

    def get_all_todos(self) -> List[Todo]:
        """Retrieve all todos in the list.

        Returns:
            List[Todo]: All todo objects (may be empty)
        """
        return self._todos.copy()

    def get_todo_by_id(self, todo_id: int) -> Todo:
        """Retrieve a specific todo by ID.

        Args:
            todo_id: The numeric identifier

        Returns:
            Todo: Todo object with matching ID

        Raises:
            NotFoundError: If no todo with matching ID exists
        """
        for todo in self._todos:
            if todo.id == todo_id:
                return todo
        raise NotFoundError(todo_id)

    def update_todo(
        self,
        todo_id: int,
        title: Optional[str] = None,
        description: Optional[str] = None
    ) -> Todo:
        """Update a todo's title and/or description.

        Args:
            todo_id: The numeric identifier
            title: New title (optional)
            description: New description (optional)

        Returns:
            Todo: Updated todo object

        Raises:
            NotFoundError: If no todo with matching ID exists
            ValueError: If title is empty or whitespace-only
        """
        todo = self.get_todo_by_id(todo_id)

        if title is not None:
            if not title or not title.strip():
                raise ValueError("Title cannot be empty")
            todo.title = title.strip()

        if description is not None:
            todo.description = description.strip() if description else ""

        return todo

    def delete_todo(self, todo_id: int) -> None:
        """Remove a todo from the list.

        Args:
            todo_id: The numeric identifier

        Raises:
            NotFoundError: If no todo with matching ID exists
        """
        todo = self.get_todo_by_id(todo_id)
        self._todos.remove(todo)

    def toggle_todo_status(self, todo_id: int) -> Todo:
        """Toggle a todo's completion status.

        Args:
            todo_id: The numeric identifier

        Returns:
            Todo: Updated todo object with flipped status

        Raises:
            NotFoundError: If no todo with matching ID exists
        """
        todo = self.get_todo_by_id(todo_id)
        todo.is_complete = not todo.is_complete
        return todo
