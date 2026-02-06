"""
Main entry point for the MCP Server for Todo Management
"""
from .src.server import TodoMCPServer
import asyncio
import argparse


def main():
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


if __name__ == "__main__":
    main()