
import random
import string
import requests
import sys

BASE_URL = "http://127.0.0.1:8000"

def get_random_string(length=8):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(length))

def test_auth():
    email = f"user_{get_random_string()}@example.com"
    password = "debugpassword123"
    
    # 1. Register
    print(f"Registering {email}...")
    try:
        reg_resp = requests.post(f"{BASE_URL}/auth/register", json={"email": email, "password": password})
        print(f"Register Status: {reg_resp.status_code}")
        print(f"Register Resp: {reg_resp.text}")
    except Exception as e:
        print(f"Register Failed: {e}")

    # 2. Login
    print(f"Logging in {email}...")
    try:
        login_resp = requests.post(f"{BASE_URL}/auth/login", json={"email": email, "password": password})
        print(f"Login Status: {login_resp.status_code}")
        print(f"Login Resp: {login_resp.text}")
        
        if login_resp.status_code == 200:
            token = login_resp.json().get("access_token")
            print("Login SUCCESS. Token received.")
            return True
        else:
            print("Login FAILED.")
            return False
            
    except Exception as e:
        print(f"Login Failed: {e}")
        return False

if __name__ == "__main__":
    success = test_auth()
    if not success:
        sys.exit(1)
