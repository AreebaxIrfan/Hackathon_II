from sqlmodel import Session, select
from src.models.todo import Todo, TodoCreate, TodoUpdate
from src.models.user import User
from typing import List, Optional
import uuid


async def create_task(session: Session, user_id: uuid.UUID, task_data: TodoCreate) -> Todo:
    """
    Create a new task for a user.
    """
    task = Todo(
        title=task_data.title,
        description=task_data.description,
        completed=task_data.completed,
        user_id=user_id
    )

    session.add(task)
    await session.commit()
    await session.refresh(task)

    return task


async def get_tasks(session: Session, user_id: uuid.UUID,
              completed: Optional[str] = "all",
              limit: int = 50, offset: int = 0) -> List[Todo]:
    """
    Get tasks for a user with optional filtering.
    """
    query = select(Todo).where(Todo.user_id == user_id)

    if completed == "pending":
        query = query.where(Todo.completed == False)
    elif completed == "completed":
        query = query.where(Todo.completed == True)

    query = query.offset(offset).limit(limit).order_by(Todo.created_at.desc())
    result = await session.exec(query)
    return result.all()


async def get_task(session: Session, task_id: uuid.UUID, user_id: uuid.UUID) -> Optional[Todo]:
    """
    Get a specific task by ID for a user.
    """
    statement = select(Todo).where(Todo.id == task_id, Todo.user_id == user_id)
    result = await session.exec(statement)
    return result.first()


async def update_task(session: Session, task_id: uuid.UUID, user_id: uuid.UUID,
                task_data: TodoUpdate) -> Optional[Todo]:
    """
    Update a task for a user.
    """
    task = await get_task(session, task_id, user_id)
    if not task:
        return None

    update_data = task_data.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(task, field, value)

    session.add(task)
    await session.commit()
    await session.refresh(task)

    return task


async def delete_task(session: Session, task_id: uuid.UUID, user_id: uuid.UUID) -> bool:
    """
    Delete a task for a user.
    """
    task = await get_task(session, task_id, user_id)
    if not task:
        return False

    await session.delete(task)
    await session.commit()

    return True


async def toggle_task_completion(session: Session, task_id: uuid.UUID, user_id: uuid.UUID,
                          completed: bool) -> Optional[Todo]:
    """
    Toggle task completion status for a user.
    """
    task = await get_task(session, task_id, user_id)
    if not task:
        return None

    task.completed = completed
    session.add(task)
    await session.commit()
    await session.refresh(task)

    return task