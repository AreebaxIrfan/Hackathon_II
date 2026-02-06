"""
MCP Server for Todo Management Tools
"""
import asyncio
from typing import Dict, Any, List, Optional
from mcps.server import MCPServer, Tool, Parameter
from .database import get_session, init_db
from .services.task_service import TaskService
from .models.task import TaskCreate, TaskUpdate
from .validation import validate_user_id, validate_task_title, validate_task_description


class TodoMCPServer:
    def __init__(self):
        self.server = MCPServer(name="Todo MCP Server")
        self._register_tools()

    def _register_tools(self):
        """Register all todo-related tools with the MCP server."""

        # add_task tool
        add_task_tool = Tool(
            name="add_task",
            description="Create a new task",
            parameters=[
                Parameter("user_id", str, required=True),
                Parameter("title", str, required=True),
                Parameter("description", str, optional=True)
            ]
        )

        # list_tasks tool
        list_tasks_tool = Tool(
            name="list_tasks",
            description="Retrieve tasks for a user",
            parameters=[
                Parameter("user_id", str, required=True),
                Parameter("status", str, optional=True)  # all, pending, completed
            ]
        )

        # complete_task tool
        complete_task_tool = Tool(
            name="complete_task",
            description="Mark a task as completed",
            parameters=[
                Parameter("user_id", str, required=True),
                Parameter("task_id", int, required=True)
            ]
        )

        # delete_task tool
        delete_task_tool = Tool(
            name="delete_task",
            description="Remove a task",
            parameters=[
                Parameter("user_id", str, required=True),
                Parameter("task_id", int, required=True)
            ]
        )

        # update_task tool
        update_task_tool = Tool(
            name="update_task",
            description="Modify a task",
            parameters=[
                Parameter("user_id", str, required=True),
                Parameter("task_id", int, required=True),
                Parameter("title", str, optional=True),
                Parameter("description", str, optional=True)
            ]
        )

        # Register tools with handlers
        self.server.register_tool(add_task_tool, self.add_task)
        self.server.register_tool(list_tasks_tool, self.list_tasks)
        self.server.register_tool(complete_task_tool, self.complete_task)
        self.server.register_tool(delete_task_tool, self.delete_task)
        self.server.register_tool(update_task_tool, self.update_task)

    async def add_task(self, user_id: str, title: str, description: str = None) -> Dict[str, Any]:
        """Add a new task."""
        # Validate inputs
        validate_user_id(user_id)
        validate_task_title(title)
        if description:
            validate_task_description(description)

        async with get_session() as session:
            task_service = TaskService(session)
            task_create = TaskCreate(user_id=user_id, title=title, description=description)
            created_task = await task_service.create_task(task_create)

            return {
                "task_id": created_task.id,
                "status": "created",
                "title": created_task.title
            }

    async def list_tasks(self, user_id: str, status: str = "all") -> Dict[str, Any]:
        """List tasks for a user."""
        # Validate inputs
        validate_user_id(user_id)
        validate_task_status(status)

        async with get_session() as session:
            task_service = TaskService(session)
            tasks = await task_service.get_tasks(user_id, status)

            return {
                "tasks": [task.model_dump() for task in tasks]
            }

    async def complete_task(self, user_id: str, task_id: int) -> Dict[str, Any]:
        """Mark a task as completed."""
        # Validate inputs
        validate_user_id(user_id)

        async with get_session() as session:
            task_service = TaskService(session)
            updated_task = await task_service.complete_task(task_id, user_id)

            return {
                "task_id": updated_task.id,
                "status": "completed",
                "title": updated_task.title
            }

    async def delete_task(self, user_id: str, task_id: int) -> Dict[str, Any]:
        """Delete a task."""
        # Validate inputs
        validate_user_id(user_id)

        async with get_session() as session:
            task_service = TaskService(session)
            success = await task_service.delete_task(task_id, user_id)

            if success:
                return {
                    "task_id": task_id,
                    "status": "deleted",
                    "title": "Deleted task"  # We can't return the title after deletion
                }
            else:
                raise ValueError(f"Task with id {task_id} not found")

    async def update_task(self, user_id: str, task_id: int, title: str = None, description: str = None) -> Dict[str, Any]:
        """Update a task."""
        # Validate inputs
        validate_user_id(user_id)
        if title is not None:
            validate_task_title(title)
        if description is not None:
            validate_task_description(description)

        update_data = {}
        if title is not None:
            update_data["title"] = title
        if description is not None:
            update_data["description"] = description

        if not update_data:
            raise ValueError("At least one field (title or description) must be provided for update")

        task_update = TaskUpdate(**update_data)

        async with get_session() as session:
            task_service = TaskService(session)
            updated_task = await task_service.update_task(task_id, user_id, task_update)

            return {
                "task_id": updated_task.id,
                "status": "updated",
                "title": updated_task.title
            }

    async def start(self, host: str = "localhost", port: int = 8001):
        """Start the MCP server."""
        await init_db()  # Initialize database on startup
        await self.server.start(host=host, port=port)

    async def stop(self):
        """Stop the MCP server."""
        await self.server.stop()


# For testing purposes
if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Todo MCP Server")
    parser.add_argument("--host", default="localhost", help="Host to bind to")
    parser.add_argument("--port", type=int, default=8001, help="Port to bind to")

    args = parser.parse_args()

    server = TodoMCPServer()

    print(f"Starting Todo MCP Server on {args.host}:{args.port}")
    try:
        asyncio.run(server.start(args.host, args.port))
    except KeyboardInterrupt:
        print("\nShutting down server...")
        asyncio.run(server.stop())