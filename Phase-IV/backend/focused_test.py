import asyncio
import os
import httpx
from openai import AsyncOpenAI
from dotenv import load_dotenv

load_dotenv()

async def main():
    api_key = os.getenv("GEMINI_API_KEY")
    base_url = "https://generativelanguage.googleapis.com/v1beta/openai/"
    model = "gemini-2.0-flash"
    
    print(f"Testing {model} at {base_url}")
    client = AsyncOpenAI(
        api_key=api_key, 
        base_url=base_url,
        http_client=httpx.AsyncClient(timeout=10.0)
    )
    try:
        response = await client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": "Hello"}],
            max_tokens=5
        )
        print(f"SUCCESS: {response.choices[0].message.content}")
    except Exception as e:
        print(f"FAILED: {e}")

if __name__ == "__main__":
    asyncio.run(main())
