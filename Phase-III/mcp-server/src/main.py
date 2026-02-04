"""
Main entry point for the MCP Server
"""
import asyncio
from mcps.server import MCPServer
from .tools.task_operations import (
    AddTaskTool,
    ListTasksTool,
    CompleteTaskTool,
    DeleteTaskTool,
    UpdateTaskTool
)


async def main():
    # Create the MCP server
    server = MCPServer(
        name="Todo Task MCP Server",
        description="MCP server for todo task operations"
    )

    # Register tools with the server
    server.register_tool(AddTaskTool())
    server.register_tool(ListTasksTool())
    server.register_tool(CompleteTaskTool())
    server.register_tool(DeleteTaskTool())
    server.register_tool(UpdateTaskTool())

    # Start the server
    print("Starting Todo Task MCP Server...")
    await server.start(host="0.0.0.0", port=8001)
    print("Server started on http://0.0.0.0:8001")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nShutting down server...")