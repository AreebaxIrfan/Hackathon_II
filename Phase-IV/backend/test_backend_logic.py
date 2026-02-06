
import asyncio
import uuid
import sys
import os

# Ensure backend directory is in python path
sys.path.append(os.getcwd())

from src.mcp.todo_tools import create_todo, read_todos, delete_todo
from src.database import init_db

# Mock user_id
USER_ID = str(uuid.uuid4())

async def test_tools():
    print(f"Testing tools for user: {USER_ID}")
    
    # 1. Create Task
    print("1. Creating task...")
    try:
        task = await create_todo(title="Direct Test Task", description="Created directly", user_id=USER_ID)
        print(f"[OK] Task created: {task['id']}")
    except Exception as e:
        import traceback
        traceback.print_exc()
        print(f"[FAIL] Failed to create task: {e}")
        return

    task_id = task['id']

    # 2. Read Tasks
    print("2. Reading tasks...")
    try:
        tasks = await read_todos(user_id=USER_ID)
        found = any(t['id'] == task_id for t in tasks)
        if found:
            print(f"[OK] Task found in list. Total tasks: {len(tasks)}")
        else:
            print(f"[FAIL] Task {task_id} not found in list!")
    except Exception as e:
        print(f"[FAIL] Failed to read tasks: {e}")

    # 3. Delete Task
    print("3. Deleting task...")
    try:
        await delete_todo(todo_id=task_id)
        print("[OK] Task deleted.")
    except Exception as e:
        print(f"[FAIL] Failed to delete task: {e}")

if __name__ == "__main__":
    if sys.platform == "win32":
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(test_tools())
