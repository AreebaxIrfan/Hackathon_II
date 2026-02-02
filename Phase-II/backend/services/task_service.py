from sqlmodel import Session, select
from models.task import Task, TaskCreate, TaskUpdate
from typing import List, Optional
import uuid


def create_task(session: Session, user_id: uuid.UUID, task_data: TaskCreate) -> Task:
    """
    Create a new task for a user.
    """
    task = Task(
        title=task_data.title,
        description=task_data.description,
        completed=task_data.completed,
        priority=task_data.priority or 1,
        user_id=user_id
    )

    session.add(task)
    session.commit()
    session.refresh(task)

    return task


def get_tasks(session: Session, user_id: uuid.UUID,
              completed: Optional[str] = "all",
              limit: int = 50, offset: int = 0,
              priority: Optional[int] = None) -> List[Task]:
    """
    Get tasks for a user with optional filtering.
    """
    query = select(Task).where(Task.user_id == user_id)

    if completed == "pending":
        query = query.where(Task.completed == False)
    elif completed == "completed":
        query = query.where(Task.completed == True)

    if priority is not None:
        query = query.where(Task.priority == priority)

    query = query.offset(offset).limit(limit).order_by(Task.created_at.desc())

    return session.exec(query).all()


def get_task(session: Session, task_id: uuid.UUID, user_id: uuid.UUID) -> Optional[Task]:
    """
    Get a specific task by ID for a user.
    """
    statement = select(Task).where(Task.id == task_id, Task.user_id == user_id)
    return session.exec(statement).first()


def update_task(session: Session, task_id: uuid.UUID, user_id: uuid.UUID,
                task_data: TaskUpdate) -> Optional[Task]:
    """
    Update a task for a user.
    """
    task = get_task(session, task_id, user_id)
    if not task:
        return None

    update_data = task_data.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(task, field, value)

    session.add(task)
    session.commit()
    session.refresh(task)

    return task


def delete_task(session: Session, task_id: uuid.UUID, user_id: uuid.UUID) -> bool:
    """
    Delete a task for a user.
    """
    task = get_task(session, task_id, user_id)
    if not task:
        return False

    session.delete(task)
    session.commit()

    return True


def toggle_task_completion(session: Session, task_id: uuid.UUID, user_id: uuid.UUID,
                          completed: bool) -> Optional[Task]:
    """
    Toggle task completion status for a user.
    """
    task = get_task(session, task_id, user_id)
    if not task:
        return None

    task.completed = completed
    session.add(task)
    session.commit()
    session.refresh(task)

    return task