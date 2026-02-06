import requests
import json
import uuid

def test_chat():
    # Use a real user ID from the database or just a random valid UUID for testing
    user_id = str(uuid.uuid4())
    url = f"http://127.0.0.1:8000/api/v1/{user_id}/chat"
    
    # We need to register this user first if the DB is fresh and chat requires a real user
    # (Though in our current logic, chat creates a conversation linked to user_id)
    # Let's try to register a user just in case
    reg_url = "http://127.0.0.1:8000/auth/register"
    email = f"test_{uuid.uuid4().hex[:8]}@example.com"
    reg_data = {"email": email, "password": "password123"}
    try:
        reg_resp = requests.post(reg_url, json=reg_data)
        if reg_resp.status_code == 201:
            user_id = reg_resp.json()["id"]
            url = f"http://127.0.0.1:8000/api/v1/{user_id}/chat"
            print(f"Registered user: {user_id}")
    except Exception as e:
        print(f"Registration skipped or failed: {e}")

    payload = {
        "message": "Hello, can you help me?",
        "conversation_id": None
    }
    
    print(f"Sending request to: {url}")
    try:
        response = requests.post(url, json=payload, timeout=30)
        print(f"Status Code: {response.status_code}")
        print(f"Response Body: {json.dumps(response.json(), indent=2)}")
    except Exception as e:
        print(f"FAILED: {e}")

if __name__ == "__main__":
    test_chat()
