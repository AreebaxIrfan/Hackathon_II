"""
MCP Tools for Task Operations
These tools will be called by the AI agent to perform task operations
"""
import asyncio
from typing import Dict, Any, List, Optional


class TaskOperations:
    """
    Class containing all task-related operations for the MCP server.
    In a real implementation, these would connect to the actual database.
    """

    def __init__(self):
        # In-memory storage for demo purposes
        self.tasks: Dict[int, Dict[str, Any]] = {}
        self.next_id = 1

    async def add_task(self, user_id: str, title: str, description: str = None) -> Dict[str, Any]:
        """Add a new task."""
        task_id = self.next_id
        self.next_id += 1

        task = {
            "id": task_id,
            "user_id": user_id,
            "title": title,
            "description": description,
            "completed": False,
            "created_at": asyncio.get_event_loop().time()  # Using current time
        }

        self.tasks[task_id] = task

        return {
            "task_id": task_id,
            "status": "created",
            "title": title
        }

    async def list_tasks(self, user_id: str, status: str = "all") -> Dict[str, Any]:
        """List tasks for a user, optionally filtered by status."""
        user_tasks = [
            task for task in self.tasks.values()
            if task["user_id"] == user_id
        ]

        if status == "pending":
            user_tasks = [task for task in user_tasks if not task["completed"]]
        elif status == "completed":
            user_tasks = [task for task in user_tasks if task["completed"]]

        return {
            "tasks": user_tasks
        }

    async def complete_task(self, user_id: str, task_id: int) -> Dict[str, Any]:
        """Mark a task as completed."""
        if task_id not in self.tasks:
            raise ValueError(f"Task with id {task_id} not found")

        task = self.tasks[task_id]

        if task["user_id"] != user_id:
            raise PermissionError("User does not have permission to modify this task")

        task["completed"] = True

        return {
            "success": True,
            "task_id": task_id,
            "status": "completed"
        }

    async def delete_task(self, user_id: str, task_id: int) -> Dict[str, Any]:
        """Delete a task."""
        if task_id not in self.tasks:
            raise ValueError(f"Task with id {task_id} not found")

        task = self.tasks[task_id]

        if task["user_id"] != user_id:
            raise PermissionError("User does not have permission to delete this task")

        del self.tasks[task_id]

        return {
            "success": True,
            "task_id": task_id
        }

    async def update_task(self, user_id: str, task_id: int, title: str = None, description: str = None) -> Dict[str, Any]:
        """Update a task."""
        if task_id not in self.tasks:
            raise ValueError(f"Task with id {task_id} not found")

        task = self.tasks[task_id]

        if task["user_id"] != user_id:
            raise PermissionError("User does not have permission to modify this task")

        if title is not None:
            task["title"] = title
        if description is not None:
            task["description"] = description

        return {
            "success": True,
            "task_id": task_id
        }


# For testing purposes
if __name__ == "__main__":
    # Demo usage
    async def demo():
        ops = TaskOperations()

        # Add a task
        result = await ops.add_task("user123", "Buy groceries", "Need to buy milk and bread")
        print("Added task:", result)

        # List tasks
        result = await ops.list_tasks("user123")
        print("Tasks:", result)

        # Complete task
        result = await ops.complete_task("user123", 1)
        print("Completed task:", result)

        # Update task
        result = await ops.update_task("user123", 1, title="Buy groceries and fruits")
        print("Updated task:", result)

    asyncio.run(demo())