
import requests
import sys
import json

BASE_URL = "http://127.0.0.1:8000"

def test_chatbot():
    # 1. Login to get token
    email = "chat_test_user@example.com"
    password = "password123"
    
    # Try register first
    requests.post(f"{BASE_URL}/auth/register", json={"email": email, "password": password})
    
    login_resp = requests.post(f"{BASE_URL}/auth/login", json={"email": email, "password": password})
    if login_resp.status_code != 200:
        print(f"Login failed: {login_resp.text}")
        return False
        
    token = login_resp.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    
    # Get User ID
    me_resp = requests.get(f"{BASE_URL}/auth/me", headers=headers)
    user_id = me_resp.json()["id"]
    
    # 2. Send Chat Message to create task
    print("Sending chat request to create task...")
    chat_payload = {
        "user_id": user_id,
        "message": "Create a task called 'Test Chatbot Task' with description 'Created via verification script'"
    }
    
    try:
        chat_resp = requests.post(f"{BASE_URL}/api/v1/{user_id}/chat", json=chat_payload, headers=headers)
        print(f"Chat Status: {chat_resp.status_code}")
        print(f"Chat Response: {chat_resp.text}")
        
        if chat_resp.status_code != 200:
            print("Chat request failed.")
            return False
            
    except Exception as e:
        print(f"Chat exception: {e}")
        return False

    # 3. Verify task exists
    print("Verifying task creation...")
    tasks_resp = requests.get(f"{BASE_URL}/api/tasks/", headers=headers)
    tasks = tasks_resp.json()
    
    found = False
    for task in tasks:
        if task["title"] == "Test Chatbot Task":
            found = True
            print(f"Found task: {task['id']}")
            break
            
    if found:
        print("SUCCESS: Chatbot created task in DB.")
        return True
    else:
        print("FAILURE: Task not found in DB.")
        return False

if __name__ == "__main__":
    if test_chatbot():
        sys.exit(0)
    else:
        sys.exit(1)
