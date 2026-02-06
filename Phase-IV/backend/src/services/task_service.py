from typing import List, Optional
import uuid
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from fastapi import HTTPException

from ..models.todo import Todo, TodoCreate, TodoUpdate, TodoRead


class TaskService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_task(self, user_id: uuid.UUID, task_create: TodoCreate) -> Todo:
        """Create a new task."""
        task = Todo(
            title=task_create.title,
            description=task_create.description,
            completed=task_create.completed,
            priority=task_create.priority,
            due_date=task_create.due_date,
            user_id=user_id
        )
        self.session.add(task)
        await self.session.commit()
        await self.session.refresh(task)

        return task

    async def get_task_by_id(self, task_id: uuid.UUID, user_id: uuid.UUID) -> Todo:
        """Get a task by ID, ensuring it belongs to the user."""
        statement = select(Todo).where(Todo.id == task_id).where(Todo.user_id == user_id)
        result = await self.session.exec(statement)
        task = result.first()

        if not task:
            raise HTTPException(status_code=404, detail="Task not found")

        return task

    async def get_tasks(self, user_id: uuid.UUID, completed: Optional[str] = "all", limit: int = 50, offset: int = 0) -> List[Todo]:
        """Get all tasks for a user, optionally filtered by status."""
        statement = select(Todo).where(Todo.user_id == user_id)

        if completed == "pending":
            statement = statement.where(Todo.completed == False)
        elif completed == "completed":
            statement = statement.where(Todo.completed == True)

        statement = statement.offset(offset).limit(limit).order_by(Todo.created_at.desc())
        result = await self.session.exec(statement)
        return result.all()

    async def update_task(self, task_id: uuid.UUID, user_id: uuid.UUID, task_update: TodoUpdate) -> Todo:
        """Update a task, ensuring it belongs to the user."""
        task = await self.get_task_by_id(task_id, user_id)

        # Update fields if they are provided in the update request
        update_data = task_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(task, field, value)

        self.session.add(task)
        await self.session.commit()
        await self.session.refresh(task)

        return task

    async def delete_task(self, task_id: uuid.UUID, user_id: uuid.UUID) -> bool:
        """Delete a task, ensuring it belongs to the user."""
        task = await self.get_task_by_id(task_id, user_id)

        await self.session.delete(task)
        await self.session.commit()

        return True

    async def toggle_task_completion(self, task_id: uuid.UUID, user_id: uuid.UUID, completed: bool) -> Todo:
        """Mark a task as completed/incomplete, ensuring it belongs to the user."""
        task = await self.get_task_by_id(task_id, user_id)

        task.completed = completed
        self.session.add(task)
        await self.session.commit()
        await self.session.refresh(task)

        return task


# Standalone function-based interface for compatibility
async def create_task(session: AsyncSession, user_id: uuid.UUID, task_data: TodoCreate) -> Todo:
    service = TaskService(session)
    return await service.create_task(user_id, task_data)

async def get_tasks(session: AsyncSession, user_id: uuid.UUID, completed: Optional[str] = "all", limit: int = 50, offset: int = 0) -> List[Todo]:
    service = TaskService(session)
    return await service.get_tasks(user_id, completed, limit, offset)

async def get_task(session: AsyncSession, task_id: uuid.UUID, user_id: uuid.UUID) -> Optional[Todo]:
    service = TaskService(session)
    try:
        return await service.get_task_by_id(task_id, user_id)
    except HTTPException:
        return None

async def update_task(session: AsyncSession, task_id: uuid.UUID, user_id: uuid.UUID, task_data: TodoUpdate) -> Optional[Todo]:
    service = TaskService(session)
    try:
        return await service.update_task(task_id, user_id, task_data)
    except HTTPException:
        return None

async def delete_task(session: AsyncSession, task_id: uuid.UUID, user_id: uuid.UUID) -> bool:
    service = TaskService(session)
    try:
        return await service.delete_task(task_id, user_id)
    except HTTPException:
        return False

async def toggle_task_completion(session: AsyncSession, task_id: uuid.UUID, user_id: uuid.UUID, completed: bool) -> Optional[Todo]:
    service = TaskService(session)
    try:
        return await service.toggle_task_completion(task_id, user_id, completed)
    except HTTPException:
        return None