
import requests
import os
from dotenv import load_dotenv

# Load .env from backend directory
load_dotenv(dotenv_path="d:\\phase-three\\Phase-III\\backend\\.env")

API_KEY = os.getenv("GEMINI_API_KEY") or os.getenv("gemini_api_key")
if not API_KEY:
    print("No API KEY found")
    print("Environment variables:", os.environ.keys())
    exit(1)

print(f"Using API Key: {API_KEY[:5]}...")

url = f"https://generativelanguage.googleapis.com/v1beta/models?key={API_KEY}"
response = requests.get(url)

if response.status_code == 200:
    models = response.json().get('models', [])
    print("\nAvailable models:")
    for m in models:
        # Check if it supports generateContent
        methods = m.get('supportedGenerationMethods', [])
        if 'generateContent' in methods:
            print(f"- {m['name']} ({m['displayName']})")
else:
    print(f"Error listing models: {response.status_code} {response.text}")
