import requests
import json

def test_chat():
    user_id = "5ba332e3-8000-05f3-44e7-892a-d9ad7c7ab490"
    url = f"http://127.0.0.1:8000/api/v1/{user_id}/chat"
    payload = {"message": "hi"}
    
    print(f"Testing {url}")
    try:
        response = requests.post(url, json=payload, timeout=30)
        print(f"Status: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_chat()
