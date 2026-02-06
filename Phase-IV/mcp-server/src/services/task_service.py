from typing import List, Optional
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from fastapi import HTTPException

from ..models.task import Task, TaskCreate, TaskUpdate, TaskRead


class TaskService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_task(self, task_create: TaskCreate) -> TaskRead:
        """Create a new task."""
        task = Task.model_validate(task_create)
        self.session.add(task)
        await self.session.commit()
        await self.session.refresh(task)

        return TaskRead.model_validate(task)

    async def get_task_by_id(self, task_id: int, user_id: str) -> Task:
        """Get a task by ID, ensuring it belongs to the user."""
        statement = select(Task).where(Task.id == task_id).where(Task.user_id == user_id)
        result = await self.session.exec(statement)
        task = result.first()

        if not task:
            raise HTTPException(status_code=404, detail="Task not found")

        return task

    async def get_tasks(self, user_id: str, status: Optional[str] = None) -> List[Task]:
        """Get all tasks for a user, optionally filtered by status."""
        statement = select(Task).where(Task.user_id == user_id)

        if status:
            if status == "pending":
                statement = statement.where(Task.completed == False)
            elif status == "completed":
                statement = statement.where(Task.completed == True)

        result = await self.session.exec(statement)
        return result.all()

    async def update_task(self, task_id: int, user_id: str, task_update: TaskUpdate) -> Task:
        """Update a task, ensuring it belongs to the user."""
        task = await self.get_task_by_id(task_id, user_id)

        # Update fields if they are provided in the update request
        update_data = task_update.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(task, field, value)

        self.session.add(task)
        await self.session.commit()
        await self.session.refresh(task)

        return task

    async def delete_task(self, task_id: int, user_id: str) -> bool:
        """Delete a task, ensuring it belongs to the user."""
        task = await self.get_task_by_id(task_id, user_id)

        await self.session.delete(task)
        await self.session.commit()

        return True

    async def complete_task(self, task_id: int, user_id: str) -> Task:
        """Mark a task as completed, ensuring it belongs to the user."""
        task = await self.get_task_by_id(task_id, user_id)

        task.completed = True
        self.session.add(task)
        await self.session.commit()
        await self.session.refresh(task)

        return task