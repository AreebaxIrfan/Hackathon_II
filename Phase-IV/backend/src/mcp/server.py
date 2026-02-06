from mcp.server import Server
from mcp.stdio import stdio_server
import asyncio


# Initialize the MCP server
server = Server(
    name="todo-mcp-server",
    version="1.0.0",
)


def start_mcp_server():
    """
    Start the MCP server.
    """
    with stdio_server(server) as shutdown_event:
        try:
            print("Starting Todo MCP Server...")
            shutdown_event.wait()
        except KeyboardInterrupt:
            print("Shutting down Todo MCP Server...")
            return


if __name__ == "__main__":
    start_mcp_server()