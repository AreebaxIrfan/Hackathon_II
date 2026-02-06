import os
from dotenv import load_dotenv

load_dotenv()
print("STARTING TEST")
key = os.getenv("GEMINI_API_KEY")
if key:
    print(f"API KEY FOUND: {key[:5]}...")
else:
    print("API KEY NOT FOUND")
print("ENDING TEST")
