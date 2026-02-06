<!--
Sync Impact Report:
Version change: 1.1.0 → 1.2.0
Modified principles: Updated all principles to reflect detailed requirements from user specification
Added sections: Database Models, Chat API Specification, MCP Tools Specification, Agent Behavior Rules, Stateless Conversation Flow, Natural Language Understanding Examples
Removed sections: None
Templates requiring updates: ⚠ pending - .specify/templates/plan-template.md, .specify/templates/spec-template.md, .specify/templates/tasks-template.md
Follow-up TODOs: None
-->
# Phase III: Todo AI Chatbot Constitution

## Core Principles

### Stateless Server Architecture
The server must be **stateless**. All conversation and task state must persist in the **database**. No server memory between requests. The chat endpoint is stateless and retrieves conversation history from the database for each request.

### AI Logic via OpenAI Agents SDK
AI logic must be implemented using the **OpenAI Agents SDK only**. The AI Agent must never directly manipulate the database. MCP tools must be the **only interface** for task CRUD operations.

### MCP-Only Task Operations
All task operations must be exposed via **MCP tools**. MCP tools must be the **only interface** for task CRUD operations. The AI Agent must never directly manipulate the database.

### User Experience and Error Handling
Every user action must receive a **friendly confirmation response**. Errors must be handled gracefully and explained in natural language. The agent must always confirm actions and explain errors politely without exposing internal system details.

### Spec-First Development
No implementation without a written and approved specification. All features and changes must be documented in spec files before any code is written.

### Agent-Driven Execution
All code is generated and modified exclusively via Claude Code using Spec-Kit Plus. No manual coding is allowed - all development must follow the Agentic Dev Stack workflow: Write spec → Generate plan → Break into tasks → Implement via Claude Code.

### User Isolation by Design
Each user can only access and modify their own tasks at all times. Database queries must always be filtered by authenticated user ID to prevent cross-user data access.

### Single Source of Truth
Specs in /specs directory are the authoritative reference for behavior and structure. All implementations must explicitly reference relevant specs using @specs/....

## Core Features

* Conversational interface for todo management
* Natural language understanding for task actions
* Persistent conversations with stateless API
* MCP-based task tools
* Resume conversations after server restart

## Technology Stack Requirements

| Component      | Technology                 |
| -------------- | -------------------------- |
| Frontend       | OpenAI ChatKit             |
| Backend        | Python FastAPI             |
| AI Framework   | OpenAI Agents SDK          |
| MCP Server     | Official MCP SDK           |
| ORM            | SQLModel                   |
| Database       | Neon Serverless PostgreSQL |
| Authentication | Better Auth                |

All components must integrate seamlessly with the MCP (Model Context Protocol) architecture.

## High-Level Architecture

**Flow:**
ChatKit UI → FastAPI Chat Endpoint → OpenAI Agent → MCP Tools → Neon Database

### Responsibilities

* **Frontend:** Collect user input & display AI responses
* **FastAPI Server:** Stateless request handling
* **Agent:** Decision-making & tool selection
* **MCP Server:** Task operations
* **Database:** Persist tasks & conversations

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

## Chat API Specification

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

## MCP Tools Specification

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

## Stateless Conversation Flow

1. Receive user message
2. Fetch conversation history from DB
3. Append new user message
4. Run agent with MCP tools
5. Store assistant response
6. Return response

⚠️ No server memory between requests

## Natural Language Understanding Examples

| User Input                    | Agent Tool               |
| ----------------------------- | ------------------------ |
| "Add a task to buy groceries" | add_task                 |
| "Show my tasks"               | list_tasks               |
| "What's pending?"             | list_tasks (pending)     |
| "Mark task 3 complete"        | complete_task            |
| "Delete the meeting task"     | list_tasks → delete_task |
| "Change task 1"               | update_task              |

## Development Workflow

- Use the Agentic Dev Stack workflow: Write spec → Generate plan → Break into tasks → Implement via Claude Code
- MCP tools must be implemented following the official MCP SDK specifications
- Database models must follow SQLModel conventions with proper relationships
- All API endpoints must follow REST conventions and properly handle JWT authentication
- AI agent behavior must follow the specified natural language command mappings
- Conversation flow must maintain statelessness while preserving context via database

## Deliverables

* GitHub Repository
* /frontend (ChatKit UI)
* /backend (FastAPI + Agents + MCP)
* /specs (Agent & MCP specifications)
* Database migrations
* README (setup & usage)

## Success Criteria

* Fully functional conversational todo chatbot
* Stateless backend
* Persistent conversations
* Correct MCP tool usage
* Clean confirmations & error handling

## Governance

This constitution governs all development activities for the Todo AI Chatbot project. All code changes, architectural decisions, and feature implementations must comply with these principles. Amendments to this constitution require explicit approval and must be documented with versioning. Development teams must verify compliance with all principles during code reviews and testing phases.

**Version**: 1.2.0 | **Ratified**: 2026-01-27 | **Last Amended**: 2026-02-04