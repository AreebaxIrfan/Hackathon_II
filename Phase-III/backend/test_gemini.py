import asyncio
import os
import httpx
from openai import AsyncOpenAI
from dotenv import load_dotenv

load_dotenv()

async def test_connection(base_url, model_name):
    api_key = os.getenv("GEMINI_API_KEY")
    print(f"\nTesting: {base_url} with model {model_name}")
    client = AsyncOpenAI(
        api_key=api_key, 
        base_url=base_url,
        http_client=httpx.AsyncClient(timeout=10.0)
    )
    try:
        response = await client.chat.completions.create(
            model=model_name,
            messages=[{"role": "user", "content": "Say hello!"}],
            max_tokens=10
        )
        print(f"SUCCESS: {response.choices[0].message.content}")
        return True
    except Exception as e:
        print(f"FAILED: {type(e).__name__}: {e}")
        return False

async def list_models(base_url):
    api_key = os.getenv("GEMINI_API_KEY")
    print(f"\nListing models for: {base_url}")
    client = AsyncOpenAI(
        api_key=api_key, 
        base_url=base_url,
        http_client=httpx.AsyncClient(timeout=10.0)
    )
    try:
        models = await client.models.list()
        print(f"AVAILABLE MODELS: {[m.id for m in models.data]}")
    except Exception as e:
        print(f"FAILED TO LIST MODELS: {type(e).__name__}: {e}")

async def main():
    base_url = "https://generativelanguage.googleapis.com/v1beta/openai/"
    await list_models(base_url)
    
    models = ["gemini-1.5-flash", "gemini-2.0-flash", "gemini-1.5-flash-8b", "gemini-2.0-flash-exp"]
    for model in models:
        await test_connection(base_url, model)

if __name__ == "__main__":
    asyncio.run(main())
