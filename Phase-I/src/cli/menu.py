"""CLI menu and display functions for Todo Console App.

This module provides all CLI-facing functions including display formatting,
menu rendering, and command handlers. Business logic is delegated to
TodoService layer - this module only handles user interaction.
"""

from typing import List
from src.models.todo import Todo
from src.services.todo_service import TodoService, NotFoundError
from src.cli.validator import validate_title, validate_id


def display_message(message: str, is_error: bool = False) -> None:
    """Display a message to the user.

    Args:
        message: The message to display
        is_error: Whether this is an error message (for formatting)
    """
    if is_error:
        print(f"✗ Error: {message}")
    else:
        print(f"✓ {message}")


def display_todos(todos: List[Todo]) -> None:
    """Display all todos in formatted list.

    Args:
        todos: List of Todo objects to display
    """
    if not todos:
        print("\nNo todos")
        return

    print("\nTodos:")
    for todo in todos:
        status = "complete" if todo.is_complete else "incomplete"
        description = f" - {todo.description}" if todo.description else ""
        print(f"  [{todo.id}] {todo.title}{description:30s} ({status})")


def display_menu() -> None:
    """Display the main CLI menu with 6 command options."""
    print("\n" + "="*40)
    print("  Todo Console App")
    print("="*40)
    print("\nCommands:")
    print("  1. Add Todo")
    print("  2. View Todos")
    print("  3. Update Todo")
    print("  4. Delete Todo")
    print("  5. Mark Complete/Incomplete")
    print("  6. Exit")


def handle_add_todo(service: TodoService) -> None:
    """Handle add todo command.

    Args:
        service: TodoService instance
    """
    print("\n--- Add Todo ---")
    try:
        title = input("Enter title: ")
        validate_title(title)

        description = input("Enter description (press Enter to skip): ")

        todo = service.create_todo(title, description)
        display_message(
            f"Todo added: [{todo.id}] {todo.title} ({'complete' if todo.is_complete else 'incomplete'})"
        )
    except ValueError as e:
        display_message(str(e), is_error=True)


def handle_view_todos(service: TodoService) -> None:
    """Handle view todos command.

    Args:
        service: TodoService instance
    """
    print("\n--- View Todos ---")
    todos = service.get_all_todos()
    display_todos(todos)


def handle_toggle_status(service: TodoService) -> None:
    """Handle toggle status command.

    Args:
        service: TodoService instance
    """
    print("\n--- Mark Complete/Incomplete ---")
    try:
        todo_id_str = input("Enter todo ID: ")
        todo_id = validate_id(todo_id_str)

        todo = service.toggle_todo_status(todo_id)
        status = "complete" if todo.is_complete else "incomplete"
        display_message(f"Todo marked as {status}: [{todo.id}] {todo.title}")
    except (ValueError, NotFoundError) as e:
        display_message(str(e), is_error=True)


def handle_update_todo(service: TodoService) -> None:
    """Handle update todo command.

    Args:
        service: TodoService instance
    """
    print("\n--- Update Todo ---")
    try:
        todo_id_str = input("Enter todo ID: ")
        todo_id = validate_id(todo_id_str)

        new_title = input("Enter new title (press Enter to keep current): ")
        new_description = input("Enter new description (press Enter to keep current): ")

        # At least one field must be provided
        if not new_title and not new_description:
            display_message("At least title or description must be provided", is_error=True)
            return

        todo = service.update_todo(
            todo_id,
            title=new_title if new_title else None,
            description=new_description if new_description else None
        )
        display_message(f"Todo updated: [{todo.id}] {todo.title} ({'complete' if todo.is_complete else 'incomplete'})")
    except (ValueError, NotFoundError) as e:
        display_message(str(e), is_error=True)


def handle_delete_todo(service: TodoService) -> None:
    """Handle delete todo command.

    Args:
        service: TodoService instance
    """
    print("\n--- Delete Todo ---")
    try:
        todo_id_str = input("Enter todo ID: ")
        todo_id = validate_id(todo_id_str)

        todo = service.get_todo_by_id(todo_id)
        service.delete_todo(todo_id)
        display_message(f"Todo deleted: [{todo.id}] {todo.title}")
    except (ValueError, NotFoundError) as e:
        display_message(str(e), is_error=True)
