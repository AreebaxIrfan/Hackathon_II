from typing import List, Optional
from sqlmodel import Session, select
from backend.src.models.task import Task, TaskCreate, TaskUpdate, TaskRead
from backend.src.db.session import get_session
from fastapi import Depends


def create_task(*, session: Session, task: TaskCreate, user_id: str) -> Task:
    """Create a new task for a user."""
    db_task = Task.from_orm(task) if hasattr(Task, 'from_orm') else Task.model_validate(task)
    db_task.user_id = user_id
    session.add(db_task)
    session.commit()
    session.refresh(db_task)
    return db_task


def get_task_by_id(*, session: Session, task_id: int, user_id: str) -> Optional[Task]:
    """Get a task by its ID if it belongs to the user."""
    statement = select(Task).where(Task.id == task_id).where(Task.user_id == user_id)
    task = session.exec(statement).first()
    return task


def get_tasks_by_user(*, session: Session, user_id: str,
                     status: Optional[str] = None,
                     sort: Optional[str] = "-created") -> List[Task]:
    """Get all tasks for a user with optional filtering and sorting."""
    statement = select(Task).where(Task.user_id == user_id)

    if status:
        if status == "completed":
            statement = statement.where(Task.completed == True)
        elif status == "pending":
            statement = statement.where(Task.completed == False)
        # If status == "all" or any other value, we don't filter

    # Apply sorting
    if sort == "created":
        statement = statement.order_by(Task.created_at.asc())
    elif sort == "-created":
        statement = statement.order_by(Task.created_at.desc())
    elif sort == "title":
        statement = statement.order_by(Task.title.asc())
    else:
        # Default sorting
        statement = statement.order_by(Task.created_at.desc())

    tasks = session.exec(statement).all()
    return tasks


def update_task(*, session: Session, task_id: int, task_update: TaskUpdate, user_id: str) -> Optional[Task]:
    """Update a task if it belongs to the user."""
    db_task = get_task_by_id(session=session, task_id=task_id, user_id=user_id)
    if not db_task:
        return None

    task_data = task_update.dict(exclude_unset=True)
    for field, value in task_data.items():
        setattr(db_task, field, value)

    session.add(db_task)
    session.commit()
    session.refresh(db_task)
    return db_task


def delete_task(*, session: Session, task_id: int, user_id: str) -> bool:
    """Delete a task if it belongs to the user."""
    db_task = get_task_by_id(session=session, task_id=task_id, user_id=user_id)
    if not db_task:
        return False

    session.delete(db_task)
    session.commit()
    return True


def toggle_task_completion(*, session: Session, task_id: int, user_id: str) -> Optional[Task]:
    """Toggle the completion status of a task."""
    db_task = get_task_by_id(session=session, task_id=task_id, user_id=user_id)
    if not db_task:
        return None

    db_task.completed = not db_task.completed
    session.add(db_task)
    session.commit()
    session.refresh(db_task)
    return db_task