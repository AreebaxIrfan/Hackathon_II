# Quickstart Guide: MCP Tools for Todo Management

## Prerequisites

- Python 3.9+
- PostgreSQL-compatible database (Neon recommended)
- MCPS library installed

## Setup Instructions

### 1. Environment Configuration
```bash
# Copy environment template
cp .env.example .env

# Update the following variables in .env:
DATABASE_URL=your_postgres_connection_string
MCP_SERVER_HOST=localhost
MCP_SERVER_PORT=8001
```

### 2. Database Setup
```bash
# Install dependencies
pip install sqlmodel alembic psycopg2-binary

# Run database migrations
alembic upgrade head
```

### 3. MCP Server Setup
```bash
# Install Python dependencies
pip install -r requirements.txt

# Start MCP server
python -m mcp_server.main
```

## Running the MCP Tools

### 1. Starting the Server
```bash
# Navigate to MCP server directory
cd mcp-server

# Start the MCP server
python -m mcp_server.main --host localhost --port 8001
```

### 2. Tool Usage Examples

#### add_task
```python
# Example call to add_task
result = await mcp_client.call_tool(
    name="add_task",
    arguments={
        "user_id": "user123",
        "title": "Buy groceries",
        "description": "Need to buy milk and bread"
    }
)
# Returns: {"task_id": 1, "status": "created", "title": "Buy groceries"}
```

#### list_tasks
```python
# Example call to list_tasks
result = await mcp_client.call_tool(
    name="list_tasks",
    arguments={
        "user_id": "user123",
        "status": "pending"
    }
)
# Returns: {"tasks": [{"id": 1, "title": "Buy groceries", ...}]}
```

#### complete_task
```python
# Example call to complete_task
result = await mcp_client.call_tool(
    name="complete_task",
    arguments={
        "user_id": "user123",
        "task_id": 1
    }
)
# Returns: {"task_id": 1, "status": "completed", "title": "Buy groceries"}
```

#### delete_task
```python
# Example call to delete_task
result = await mcp_client.call_tool(
    name="delete_task",
    arguments={
        "user_id": "user123",
        "task_id": 1
    }
)
# Returns: {"task_id": 1, "status": "deleted", "title": "Buy groceries"}
```

#### update_task
```python
# Example call to update_task
result = await mcp_client.call_tool(
    name="update_task",
    arguments={
        "user_id": "user123",
        "task_id": 1,
        "title": "Buy groceries and fruits"
    }
)
# Returns: {"task_id": 1, "status": "updated", "title": "Buy groceries and fruits"}
```

## Testing the MCP Tools

### Running Unit Tests
```bash
# Run unit tests for MCP tools
pytest tests/unit/test_mcp_tools.py
```

### Running Integration Tests
```bash
# Run integration tests
pytest tests/integration/test_mcp_integration.py
```

## Troubleshooting

### Common Issues
- **Database Connection Issues**: Check DATABASE_URL in environment variables
- **User Access Errors**: Verify user_id matches the task owner
- **Invalid Parameters**: Check that required parameters are provided
- **Server Not Responding**: Verify MCP server is running and accessible

### Logs
- MCP server logs: Check console output from MCP server
- Error logs: Located in logs/mcp_server.log