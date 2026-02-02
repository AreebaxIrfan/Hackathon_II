import pytest
from fastapi.testclient import TestClient
from sqlmodel import create_engine, Session
from sqlalchemy.pool import StaticPool
from unittest.mock import MagicMock, patch
import uuid

from main import app
from database.session import get_session
from models.task import Task


# Create an in-memory SQLite database for testing
@pytest.fixture(name="session")
def session_fixture():
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    SQLModel.metadata.create_all(bind=engine)
    with Session(engine) as session:
        yield session


@pytest.fixture(name="client")
def client_fixture(session: Session):
    def get_session_override():
        yield session

    app.dependency_overrides[get_session] = get_session_override
    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()


def test_create_task(client: TestClient):
    """Test creating a new task"""
    # Mock user authentication
    mock_user_id = uuid.uuid4()

    with patch('auth.dependencies.get_current_user') as mock_auth:
        mock_auth.return_value = {"user_id": mock_user_id}

        # Test task creation
        response = client.post(
            "/api/tasks/",
            json={
                "title": "Test Task",
                "description": "Test Description",
                "priority": 3
            },
            headers={"Authorization": "Bearer fake-token"}
        )

        assert response.status_code == 201
        data = response.json()
        assert data["title"] == "Test Task"
        assert data["description"] == "Test Description"
        assert data["priority"] == 3
        assert data["user_id"] == str(mock_user_id)
        assert data["completed"] is False


def test_get_user_tasks(client: TestClient, session: Session):
    """Test getting user's tasks"""
    # Create a mock user and tasks
    mock_user_id = uuid.uuid4()

    # Add some tasks to the database
    task1 = Task(
        title="Task 1",
        description="Description 1",
        completed=False,
        priority=1,
        user_id=mock_user_id
    )
    task2 = Task(
        title="Task 2",
        description="Description 2",
        completed=True,
        priority=2,
        user_id=mock_user_id
    )

    session.add(task1)
    session.add(task2)
    session.commit()

    with patch('auth.dependencies.get_current_user') as mock_auth:
        mock_auth.return_value = {"user_id": mock_user_id}

        # Test getting user's tasks
        response = client.get("/api/tasks/", headers={"Authorization": "Bearer fake-token"})

        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2

        # Verify task details
        titles = [task["title"] for task in data]
        assert "Task 1" in titles
        assert "Task 2" in titles


def test_update_task(client: TestClient, session: Session):
    """Test updating a task"""
    # Create a mock user and task
    mock_user_id = uuid.uuid4()

    task = Task(
        title="Original Task",
        description="Original Description",
        completed=False,
        priority=1,
        user_id=mock_user_id
    )

    session.add(task)
    session.commit()

    with patch('auth.dependencies.get_current_user') as mock_auth:
        mock_auth.return_value = {"user_id": mock_user_id}

        # Test updating the task
        response = client.put(
            f"/api/tasks/{task.id}",
            json={
                "title": "Updated Task",
                "description": "Updated Description",
                "completed": True,
                "priority": 5
            },
            headers={"Authorization": "Bearer fake-token"}
        )

        assert response.status_code == 200
        data = response.json()
        assert data["title"] == "Updated Task"
        assert data["description"] == "Updated Description"
        assert data["completed"] is True
        assert data["priority"] == 5


def test_delete_task(client: TestClient, session: Session):
    """Test deleting a task"""
    # Create a mock user and task
    mock_user_id = uuid.uuid4()

    task = Task(
        title="Task to Delete",
        description="Description",
        completed=False,
        priority=1,
        user_id=mock_user_id
    )

    session.add(task)
    session.commit()

    with patch('auth.dependencies.get_current_user') as mock_auth:
        mock_auth.return_value = {"user_id": mock_user_id}

        # Test deleting the task
        response = client.delete(f"/api/tasks/{task.id}", headers={"Authorization": "Bearer fake-token"})

        assert response.status_code == 200
        assert response.json()["message"] == "Task deleted successfully"


def test_complete_task(client: TestClient, session: Session):
    """Test marking a task as complete"""
    # Create a mock user and task
    mock_user_id = uuid.uuid4()

    task = Task(
        title="Incomplete Task",
        description="Description",
        completed=False,
        priority=1,
        user_id=mock_user_id
    )

    session.add(task)
    session.commit()

    with patch('auth.dependencies.get_current_user') as mock_auth:
        mock_auth.return_value = {"user_id": mock_user_id}

        # Test completing the task
        response = client.patch(f"/api/tasks/{task.id}/complete", headers={"Authorization": "Bearer fake-token"})

        assert response.status_code == 200
        data = response.json()
        assert data["completed"] is True


def test_incomplete_task(client: TestClient, session: Session):
    """Test marking a task as incomplete"""
    # Create a mock user and task
    mock_user_id = uuid.uuid4()

    task = Task(
        title="Complete Task",
        description="Description",
        completed=True,
        priority=1,
        user_id=mock_user_id
    )

    session.add(task)
    session.commit()

    with patch('auth.dependencies.get_current_user') as mock_auth:
        mock_auth.return_value = {"user_id": mock_user_id}

        # Test marking the task as incomplete
        response = client.patch(f"/api/tasks/{task.id}/incomplete", headers={"Authorization": "Bearer fake-token"})

        assert response.status_code == 200
        data = response.json()
        assert data["completed"] is False