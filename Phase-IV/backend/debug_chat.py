
import requests
import json

BASE_URL = "http://127.0.0.1:8000"
email = "debug_chat@example.com"
password = "password123"

def debug():
    print("1. Registering/Logging in...")
    requests.post(f"{BASE_URL}/auth/register", json={"email": email, "password": password})
    login_resp = requests.post(f"{BASE_URL}/auth/login", json={"email": email, "password": password})
    token = login_resp.json()["access_token"]
    
    me_resp = requests.get(f"{BASE_URL}/auth/me", headers={"Authorization": f"Bearer {token}"})
    user_id = me_resp.json()["id"]
    print(f"Logged in as user: {user_id}")
    
    print("2. Sending Chat Request...")
    chat_resp = requests.post(
        f"{BASE_URL}/api/v1/{user_id}/chat",
        json={"message": "hello", "conversation_id": None},
        headers={"Authorization": f"Bearer {token}"}
    )
    print(f"Status: {chat_resp.status_code}")
    print(f"Response: {json.dumps(chat_resp.json(), indent=2)}")

if __name__ == "__main__":
    debug()
