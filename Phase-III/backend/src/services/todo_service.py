from typing import List, Optional
from sqlmodel import Session, select
from backend.src.models.todo import Todo, TodoCreate, TodoUpdate
from uuid import UUID


class TodoService:
    @staticmethod
    def create_todo(session: Session, todo_create: TodoCreate, user_id: UUID) -> Todo:
        """
        Create a new todo for a user.
        """
        todo = Todo.model_validate(todo_create)
        todo.user_id = user_id
        session.add(todo)
        session.commit()
        session.refresh(todo)
        return todo

    @staticmethod
    def get_todos_by_user(session: Session, user_id: UUID) -> List[Todo]:
        """
        Get all todos for a specific user.
        """
        statement = select(Todo).where(Todo.user_id == user_id)
        return session.exec(statement).all()

    @staticmethod
    def get_todo_by_id(session: Session, todo_id: UUID, user_id: UUID) -> Optional[Todo]:
        """
        Get a specific todo by ID for a specific user.
        """
        statement = select(Todo).where(Todo.id == todo_id, Todo.user_id == user_id)
        return session.exec(statement).first()

    @staticmethod
    def update_todo(session: Session, todo_id: UUID, todo_update: TodoUpdate, user_id: UUID) -> Optional[Todo]:
        """
        Update a specific todo for a user.
        """
        todo = TodoService.get_todo_by_id(session, todo_id, user_id)
        if not todo:
            return None

        update_data = todo_update.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(todo, field, value)

        session.add(todo)
        session.commit()
        session.refresh(todo)
        return todo

    @staticmethod
    def delete_todo(session: Session, todo_id: UUID, user_id: UUID) -> bool:
        """
        Delete a specific todo for a user.
        """
        todo = TodoService.get_todo_by_id(session, todo_id, user_id)
        if not todo:
            return False

        session.delete(todo)
        session.commit()
        return True