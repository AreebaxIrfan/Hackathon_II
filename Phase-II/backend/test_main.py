from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert "message" in response.json()

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}

def test_register_endpoint_exists():
    # Just check that the endpoint accepts requests (without actually registering)
    response = client.post("/auth/register", json={
        "email": "test@example.com",
        "password": "testpassword"
    })
    # Expect 422 for validation error or 400 for user exists, but not 404
    assert response.status_code in [400, 422]

def test_login_endpoint_exists():
    # Just check that the endpoint accepts requests (without actually logging in)
    response = client.post("/auth/login", json={
        "email": "test@example.com",
        "password": "testpassword"
    })
    # Expect 401 for invalid credentials, but not 404
    assert response.status_code == 401