"""
Basic API tests for the Chat Flow API
"""
import pytest
import asyncio
from fastapi.testclient import TestClient
from src.main import app


@pytest.fixture
def client():
    """Create a test client for the API."""
    with TestClient(app) as test_client:
        yield test_client


def test_root_endpoint(client):
    """Test the root endpoint."""
    response = client.get("/")
    assert response.status_code == 200
    assert "message" in response.json()


def test_health_endpoint(client):
    """Test the health check endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_chat_endpoint_exists(client):
    """Test that the chat endpoint exists."""
    # This will fail with 422 because we're not providing required parameters,
    # but it verifies the endpoint exists
    response = client.post("/api/user123/chat")
    assert response.status_code in [422, 500]  # Either validation error or internal error due to missing dependencies