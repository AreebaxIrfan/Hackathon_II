# Quickstart Guide for Database Schema & Persistence

## Prerequisites
- Python 3.7+
- PostgreSQL-compatible database (Neon)
- SQLModel installed
- Environment variables configured

## Database Setup
1. Set up Neon PostgreSQL database
2. Configure environment variables:
   ```
   DATABASE_URL=postgresql://username:password@host:port/database_name
   ```

## Model Initialization
1. Define SQLModel models for User and Task entities
2. Create database tables using SQLModel's metadata
3. Set up Alembic for migrations if needed

## Connection Configuration
1. Create database session factory
2. Implement connection pooling
3. Handle connection lifecycle properly

## Example Usage
```python
from sqlmodel import Session, select
from models.user import User
from models.task import Task
from database.session import engine

# Create a new user
with Session(engine) as session:
    user = User(email="user@example.com", hashed_password="hashed_password")
    session.add(user)
    session.commit()
    session.refresh(user)

# Create a task for the user
with Session(engine) as session:
    task = Task(title="Sample Task", user_id=user.id)
    session.add(task)
    session.commit()

# Retrieve user's tasks
with Session(engine) as session:
    tasks = session.exec(select(Task).where(Task.user_id == user.id)).all()
```

## Validation
- Verify data persistence works correctly
- Test user-scoped queries perform efficiently
- Confirm foreign key relationships enforce data integrity
- Ensure cascade delete behavior works as expected