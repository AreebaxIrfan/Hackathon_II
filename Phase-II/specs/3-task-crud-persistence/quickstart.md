# Quickstart Guide for Task CRUD & Data Persistence

## Overview

This guide walks through implementing the Task CRUD & Data Persistence feature with user isolation and PostgreSQL storage.

## Prerequisites

- Python 3.9+ for backend
- PostgreSQL database
- Understanding of SQLModel and FastAPI
- Existing authentication system with JWT support

## Backend Setup

### 1. Install Dependencies

```bash
pip install fastapi sqlmodel pydantic python-jose[cryptography] passlib[bcrypt] psycopg2-binary
```

### 2. Set Up Database Models

Create the Task model with proper user association:

```python
from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime
import uuid

class TaskBase(SQLModel):
    title: str = Field(min_length=1, max_length=255)
    description: Optional[str] = Field(default=None, max_length=1000)
    completed: bool = Field(default=False)
    priority: Optional[int] = Field(default=1, ge=1, le=5)

class Task(TaskBase, table=True):
    """
    Task model representing user tasks with completion status and priority.
    """
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    user_id: uuid.UUID = Field(foreign_key="user.id", nullable=False)
    created_at: Optional[datetime] = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = Field(default_factory=datetime.utcnow)
```

### 3. Create Pydantic Schemas

```python
from pydantic import BaseModel
from typing import Optional
from datetime import datetime
import uuid

class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None
    completed: bool = False
    priority: Optional[int] = 1

class TaskCreate(TaskBase):
    title: str

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None
    priority: Optional[int] = None

class TaskResponse(TaskBase):
    id: uuid.UUID
    user_id: uuid.UUID
    created_at: datetime
    updated_at: datetime
```

## API Implementation

### 1. Create Task Service Layer

```python
from sqlmodel import Session, select
from models.task import Task, TaskCreate
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
              limit: int = 50, offset: int = 0) -> List[Task]:
    """
    Get tasks for a user with optional filtering.
    """
    query = select(Task).where(Task.user_id == user_id)

    if completed == "pending":
        query = query.where(Task.completed == False)
    elif completed == "completed":
        query = query.where(Task.completed == True)

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
```

### 2. Create Task API Endpoints

```python
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer
from sqlmodel import Session
from typing import List, Optional
import uuid

from database.session import get_session
from auth.dependencies import get_current_user
from services.task_service import create_task, get_tasks, get_task, update_task, delete_task
from schemas.task import TaskCreate, TaskUpdate, TaskResponse

router = APIRouter()
security = HTTPBearer()

@router.get("/", response_model=List[TaskResponse])
def get_user_tasks(
    completed: Optional[str] = "all",
    limit: int = 50,
    offset: int = 0,
    current_user: dict = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Get tasks for the authenticated user.
    """
    tasks = get_tasks(
        session=session,
        user_id=current_user["user_id"],
        completed=completed,
        limit=limit,
        offset=offset
    )
    return tasks

@router.post("/", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
def create_user_task(
    task_data: TaskCreate,
    current_user: dict = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Create a new task for the authenticated user.
    """
    task = create_task(
        session=session,
        user_id=current_user["user_id"],
        task_data=task_data
    )
    return task

@router.get("/{task_id}", response_model=TaskResponse)
def get_specific_task(
    task_id: uuid.UUID,
    current_user: dict = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Get a specific task by ID for the authenticated user.
    """
    task = get_task(
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

@router.put("/{task_id}", response_model=TaskResponse)
def update_user_task(
    task_id: uuid.UUID,
    task_data: TaskUpdate,
    current_user: dict = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Update a task for the authenticated user.
    """
    updated_task = update_task(
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
def delete_user_task(
    task_id: uuid.UUID,
    current_user: dict = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Delete a task for the authenticated user.
    """
    success = delete_task(
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
```

## Security Implementation

### 1. User Isolation

All database queries must include user ID filtering to ensure user isolation:

```python
# Example query with user isolation
statement = select(Task).where(Task.user_id == current_user["user_id"])
```

### 2. Ownership Verification

Verify ownership before allowing modifications:

```python
def verify_task_ownership(session: Session, task_id: uuid.UUID, user_id: uuid.UUID) -> bool:
    """
    Verify that the user owns the task.
    """
    task = session.get(Task, task_id)
    return task and task.user_id == user_id
```

## Testing

### 1. Create Test Cases

```python
def test_create_task():
    # Test task creation for authenticated user
    pass

def test_get_user_tasks():
    # Test retrieving only user's tasks
    pass

def test_task_isolation():
    # Test that users can't access other users' tasks
    pass

def test_update_task():
    # Test updating user's own tasks
    pass

def test_delete_task():
    # Test deleting user's own tasks
    pass
```

## Deployment

1. Set up PostgreSQL database with proper credentials
2. Configure environment variables for database connection
3. Run database migrations
4. Deploy backend application
5. Configure authentication system to work with task endpoints

## Error Handling

- Return 401 Unauthorized for unauthenticated requests
- Return 403 Forbidden for unauthorized access attempts
- Return 404 Not Found for non-existent tasks
- Return 422 Unprocessable Entity for validation errors
- Use consistent error response format across all endpoints