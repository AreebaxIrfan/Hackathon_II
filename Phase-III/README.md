# Phase III: Todo AI Chatbot

A stateless, AI-powered Todo Chatbot using MCP (Model Context Protocol) and the OpenAI Agents SDK.

## Architecture

**Flow:**
ChatKit UI → FastAPI Chat Endpoint → OpenAI Agent → MCP Tools → Neon Database

## Components

- **Frontend**: OpenAI ChatKit
- **Backend**: Python FastAPI
- **AI Framework**: OpenAI Agents SDK
- **MCP Server**: Official MCP SDK
- **ORM**: SQLModel
- **Database**: Neon Serverless PostgreSQL
- **Authentication**: Better Auth

## Features

- Conversational interface for todo management
- Natural language understanding for task actions
- Persistent conversations with stateless API
- MCP-based task tools
- Resume conversations after server restart

## Setup

1. **Environment Variables**:
   ```bash
   cp .env.example .env
   # Update the values in .env
   ```

2. **Backend**:
   ```bash
   cd backend
   pip install -r requirements.txt
   uvicorn src.main:app --reload
   ```

3. **MCP Server**:
   ```bash
   cd mcp-server
   pip install -r requirements.txt
   python src/server.py
   ```

4. **Frontend**:
   ```bash
   cd frontend
   npm install
   npm run dev
   ```

## Database Models

### Task
| Field       | Description      |
| ----------- | ---------------- |
| id          | Primary key      |
| user_id     | Owner of task    |
| title       | Task title       |
| description | Optional details |
| completed   | Boolean status   |
| created_at  | Creation time    |
| updated_at  | Last update time |

### Conversation
| Field      | Description       |
| ---------- | ----------------- |
| id         | Conversation ID   |
| user_id    | Owner             |
| created_at | Start time        |
| updated_at | Last message time |

### Message
| Field           | Description         |
| --------------- | ------------------- |
| id              | Message ID          |
| user_id         | Owner               |
| conversation_id | Linked conversation |
| role            | user / assistant    |
| content         | Message text        |
| created_at      | Timestamp           |

## API Specification

### Endpoint

`POST /api/{user_id}/chat`

### Request Body

| Field           | Required | Description                      |
| --------------- | -------- | -------------------------------- |
| conversation_id | No       | Existing conversation (optional) |
| message         | Yes      | User natural language input      |

### Response Body

| Field           | Description            |
| --------------- | ---------------------- |
| conversation_id | Active conversation ID |
| response        | Assistant reply        |
| tool_calls      | MCP tools invoked      |

## MCP Tools

### Tool: add_task

**Purpose:** Create a new task

**Parameters:**

* user_id (string, required)
* title (string, required)
* description (string, optional)

**Returns:** task_id, status, title

### Tool: list_tasks

**Purpose:** Retrieve tasks

**Parameters:**

* user_id (string, required)
* status (optional: all | pending | completed)

**Returns:** Array of task objects

### Tool: complete_task

**Purpose:** Mark task as completed

**Parameters:**

* user_id (string, required)
* task_id (integer, required)

### Tool: delete_task

**Purpose:** Remove task

**Parameters:**

* user_id (string, required)
* task_id (integer, required)

### Tool: update_task

**Purpose:** Modify task

**Parameters:**

* user_id (string, required)
* task_id (integer, required)
* title (optional)
* description (optional)

## Agent Behavior Rules

| Scenario         | Agent Action            |
| ---------------- | ----------------------- |
| Add task         | Call add_task           |
| List tasks       | Call list_tasks         |
| Complete task    | Call complete_task      |
| Delete task      | Call delete_task        |
| Update task      | Call update_task        |
| Ambiguous delete | List first, then delete |

The agent must:

* Always confirm actions
* Explain errors politely
* Never expose internal system details

## Natural Language Understanding Examples

| User Input                    | Agent Tool               |
| ----------------------------- | ------------------------ |
| "Add a task to buy groceries" | add_task                 |
| "Show my tasks"               | list_tasks               |
| "What's pending?"             | list_tasks (pending)     |
| "Mark task 3 complete"        | complete_task            |
| "Delete the meeting task"     | list_tasks → delete_task |
| "Change task 1"               | update_task              |
