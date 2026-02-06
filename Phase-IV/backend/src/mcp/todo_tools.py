from typing import Dict, Any, List
# Removed mcp import since we are running standalone

from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from src.models.todo import Todo, TodoCreate
from src.database import engine
from uuid import UUID


async def create_todo(title: str, description: str = None, user_id: str = None) -> Dict[str, Any]:
    """
    Create a new todo for the user.
    """
    async with AsyncSession(engine) as session:
        try:
            # Create the todo
            # Create the todo
            todo = Todo(
                title=title,
                description=description,
                user_id=UUID(user_id) if user_id else None
            )

            session.add(todo)
            await session.commit()
            await session.refresh(todo)

            return {
                "id": str(todo.id),
                "title": todo.title,
                "description": todo.description,
                "completed": todo.completed,
                "user_id": str(todo.user_id) if todo.user_id else None,
                "created_at": todo.created_at.isoformat() if todo.created_at else None,
                "updated_at": todo.updated_at.isoformat() if todo.updated_at else None
            }
        except Exception as e:
            raise Exception(f"Failed to create todo: {str(e)}")


async def read_todos(user_id: str = None, filters: Dict[str, Any] = None) -> List[Dict[str, Any]]:
    """
    Read todos for the user.
    """
    async with AsyncSession(engine) as session:
        try:
            statement = select(Todo)
            if user_id:
                statement = statement.where(Todo.user_id == UUID(user_id))

            if filters:
                # Apply filters if provided
                if filters.get("completed") is not None:
                    statement = statement.where(Todo.completed == filters["completed"])

            result = await session.exec(statement)
            todos = result.all()

            return [
                {
                    "id": str(todo.id),
                    "title": todo.title,
                    "description": todo.description,
                    "completed": todo.completed,
                    "user_id": str(todo.user_id) if todo.user_id else None,
                    "created_at": todo.created_at.isoformat() if todo.created_at else None,
                    "updated_at": todo.updated_at.isoformat() if todo.updated_at else None
                }
                for todo in todos
            ]
        except Exception as e:
            raise Exception(f"Failed to read todos: {str(e)}")


async def update_todo(todo_id: str, updates: Dict[str, Any]) -> Dict[str, Any]:
    """
    Update an existing todo.
    """
    async with AsyncSession(engine) as session:
        try:
            # Get the todo
            todo = await session.get(Todo, UUID(todo_id))
            if not todo:
                raise Exception(f"Todo with id {todo_id} not found")

            # Apply updates
            for field, value in updates.items():
                if hasattr(todo, field):
                    setattr(todo, field, value)

            session.add(todo)
            await session.commit()
            await session.refresh(todo)

            return {
                "id": str(todo.id),
                "title": todo.title,
                "description": todo.description,
                "completed": todo.completed,
                "user_id": str(todo.user_id) if todo.user_id else None,
                "created_at": todo.created_at.isoformat() if todo.created_at else None,
                "updated_at": todo.updated_at.isoformat() if todo.updated_at else None
            }
        except Exception as e:
            raise Exception(f"Failed to update todo: {str(e)}")


async def delete_todo(todo_id: str) -> bool:
    """
    Delete a todo.
    """
    async with AsyncSession(engine) as session:
        try:
            # Get the todo
            todo = await session.get(Todo, UUID(todo_id))
            if not todo:
                raise Exception(f"Todo with id {todo_id} not found")

            await session.delete(todo)
            await session.commit()

            return True
        except Exception as e:
            raise Exception(f"Failed to delete todo: {str(e)}")


# Add .name attribute for Agent compatibility since we removed @server.tool decorator
create_todo.name = "create_todo"
read_todos.name = "read_todos"
update_todo.name = "update_todo"
delete_todo.name = "delete_todo"