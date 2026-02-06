# MCP Server for Todo Management

MCP (Model Context Protocol) server that exposes task operations as tools for the AI agent.

## Tools Available

- `add_task` - Create a new task
- `list_tasks` - Retrieve tasks for a user
- `complete_task` - Mark a task as completed
- `delete_task` - Remove a task
- `update_task` - Modify a task

## Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Set up environment:
   ```bash
   cp .env.example .env
   # Update the values in .env
   ```

3. Run the server:
   ```bash
   python -m mcp_server.main
   ```

## Tool Specifications

### add_task
- **Purpose**: Create a new task
- **Parameters**:
  - `user_id` (required string)
  - `title` (required string)
  - `description` (optional string)
- **Returns**: `task_id`, `status` ("created"), `title`

### list_tasks
- **Purpose**: Retrieve tasks
- **Parameters**:
  - `user_id` (required string)
  - `status` (optional string: all|pending|completed)
- **Returns**: Array of task objects

### complete_task
- **Purpose**: Mark task as completed
- **Parameters**:
  - `user_id` (required string)
  - `task_id` (required integer)
- **Returns**: `task_id`, `status` ("completed"), `title`

### delete_task
- **Purpose**: Remove task
- **Parameters**:
  - `user_id` (required string)
  - `task_id` (required integer)
- **Returns**: `task_id`, `status` ("deleted"), `title`

### update_task
- **Purpose**: Modify task
- **Parameters**:
  - `user_id` (required string)
  - `task_id` (required integer)
  - `title` (optional string)
  - `description` (optional string)
- **Returns**: `task_id`, `status` ("updated"), `title`

## Configuration

The server runs on `localhost:8001` by default.