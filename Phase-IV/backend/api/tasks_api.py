from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
import uuid
from sqlmodel.ext.asyncio.session import AsyncSession
from src.database import get_session
from auth.dependencies import get_current_user
from src.models.todo import Todo, TodoCreate, TodoUpdate, TodoRead
from src.services.task_service import (
    create_task, get_tasks, get_task, update_task, delete_task, toggle_task_completion
)

router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.post("/", response_model=TodoRead, status_code=status.HTTP_201_CREATED)
async def create_user_task(
    task_data: TodoCreate,
    current_user: dict = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
):
    """
    Create a new task for the authenticated user.
    """
    task = await create_task(
        session=session,
        user_id=current_user["user_id"],
        task_data=task_data
    )
    return task


@router.get("/", response_model=List[TodoRead])
async def get_user_tasks(
    completed: str = "all",
    limit: int = 50,
    offset: int = 0,
    priority: int = None,
    current_user: dict = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
):
    """
    Get tasks for the authenticated user.
    """
    tasks = await get_tasks(
        session=session,
        user_id=current_user["user_id"],
        completed=completed,
        limit=limit,
        offset=offset
    )
    return tasks


@router.get("/{task_id}", response_model=TodoRead)
async def get_specific_task(
    task_id: uuid.UUID,
    current_user: dict = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
):
    """
    Get a specific task by ID for the authenticated user.
    """
    task = await get_task(
        session=session,
        task_id=task_id,
        user_id=current_user["user_id"]
    )
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )
    return task


@router.put("/{task_id}", response_model=TodoRead)
async def update_user_task(
    task_id: uuid.UUID,
    task_data: TodoUpdate,
    current_user: dict = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
):
    """
    Update a task for the authenticated user.
    """
    updated_task = await update_task(
        session=session,
        task_id=task_id,
        user_id=current_user["user_id"],
        task_data=task_data
    )
    if not updated_task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )
    return updated_task


@router.delete("/{task_id}")
async def delete_user_task(
    task_id: uuid.UUID,
    current_user: dict = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
):
    """
    Delete a task for the authenticated user.
    """
    success = await delete_task(
        session=session,
        task_id=task_id,
        user_id=current_user["user_id"]
    )
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )
    return {"message": "Task deleted successfully"}


@router.patch("/{task_id}/complete", response_model=TodoRead)
async def complete_user_task(
    task_id: uuid.UUID,
    current_user: dict = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
):
    """
    Mark a task as complete for the authenticated user.
    """
    updated_task = await toggle_task_completion(
        session=session,
        task_id=task_id,
        user_id=current_user["user_id"],
        completed=True
    )
    if not updated_task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )
    return updated_task


@router.patch("/{task_id}/incomplete", response_model=TodoRead)
async def incomplete_user_task(
    task_id: uuid.UUID,
    current_user: dict = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
):
    """
    Mark a task as incomplete for the authenticated user.
    """
    updated_task = await toggle_task_completion(
        session=session,
        task_id=task_id,
        user_id=current_user["user_id"],
        completed=False
    )
    if not updated_task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )
    return updated_task