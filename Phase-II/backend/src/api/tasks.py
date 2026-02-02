from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlmodel import Session
from typing import List, Optional
from backend.src.db.session import get_session
from backend.src.api.deps import get_current_user_id
from backend.src.models.task import Task, TaskCreate, TaskUpdate, TaskRead
from backend.src.services.task_service import (
    create_task,
    get_task_by_id,
    get_tasks_by_user,
    update_task,
    delete_task,
    toggle_task_completion
)

router = APIRouter()


@router.get("/", response_model=List[TaskRead])
def list_tasks(
    user_id: str = Depends(get_current_user_id),
    status: Optional[str] = Query(None, description="Filter by status: pending|completed|all"),
    sort: Optional[str] = Query("-created", description="Sort by: created|title|-created"),
    session: Session = Depends(get_session)
):
    """
    List authenticated user's tasks.
    """
    tasks = get_tasks_by_user(session=session, user_id=user_id, status=status, sort=sort)
    return tasks


@router.post("/", response_model=TaskRead, status_code=status.HTTP_201_CREATED)
def create_task_endpoint(
    task: TaskCreate,
    user_id: str = Depends(get_current_user_id),
    session: Session = Depends(get_session)
):
    """
    Create a new task for authenticated user.
    """
    db_task = create_task(session=session, task=task, user_id=user_id)
    return db_task


@router.get("/{task_id}", response_model=TaskRead)
def get_task(
    task_id: int,
    user_id: str = Depends(get_current_user_id),
    session: Session = Depends(get_session)
):
    """
    Get a specific task by ID.
    """
    task = get_task_by_id(session=session, task_id=task_id, user_id=user_id)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found or you don't have permission to access it"
        )
    return task


@router.put("/{task_id}", response_model=TaskRead)
def update_task_endpoint(
    task_id: int,
    task_update: TaskUpdate,
    user_id: str = Depends(get_current_user_id),
    session: Session = Depends(get_session)
):
    """
    Update a specific task by ID.
    """
    updated_task = update_task(session=session, task_id=task_id, task_update=task_update, user_id=user_id)
    if not updated_task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found or you don't have permission to access it"
        )
    return updated_task


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task_endpoint(
    task_id: int,
    user_id: str = Depends(get_current_user_id),
    session: Session = Depends(get_session)
):
    """
    Delete a specific task by ID.
    """
    success = delete_task(session=session, task_id=task_id, user_id=user_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found or you don't have permission to access it"
        )
    return


@router.patch("/{task_id}/complete", response_model=TaskRead)
def toggle_task_complete(
    task_id: int,
    user_id: str = Depends(get_current_user_id),
    session: Session = Depends(get_session)
):
    """
    Toggle completion status of a specific task.
    """
    task = toggle_task_completion(session=session, task_id=task_id, user_id=user_id)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found or you don't have permission to access it"
        )
    return task