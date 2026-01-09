"""Main entry point for Todo Console App.

This module provides CLI orchestration only. All business logic is
delegated to TodoService layer. Handles command routing, user input
parsing, and application lifecycle.
"""

from src.services.todo_service import TodoService
from src.cli.menu import (
    display_menu,
    handle_add_todo,
    handle_view_todos,
    handle_update_todo,
    handle_delete_todo,
    handle_toggle_status,
)


def main() -> None:
    """Main CLI loop for Todo Console App.

    Orchestrates user interaction by displaying menu, parsing commands,
    and delegating to appropriate handler functions. No business logic
    in this module - only CLI routing.
    
    """
    service = TodoService()

    while True:
        display_menu()
        try:
            command = input("\nEnter command (1-6): ").strip()

            if command == "1":
                handle_add_todo(service)
            elif command == "2":
                handle_view_todos(service)
            elif command == "3":
                handle_update_todo(service)
            elif command == "4":
                handle_delete_todo(service)
            elif command == "5":
                handle_toggle_status(service)
            elif command == "6":
                print("\nGoodbye!")
                break
            else:
                print("Invalid command. Please enter a number between 1 and 6.")
        except KeyboardInterrupt:
            print("\n\nGoodbye!")
            break
        except Exception as e:
            print(f"\n✗ Unexpected error: {e}")
            print("Please try again.")


if __name__ == "__main__":
    main()
