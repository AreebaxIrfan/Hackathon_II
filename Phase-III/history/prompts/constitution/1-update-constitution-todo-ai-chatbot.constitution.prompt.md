---
id: 1
title: "update-constitution-todo-ai-chatbot"
stage: "constitution"
date_iso: "2026-02-04"
surface: "agent"
model: "Sonnet 4.5"
feature: "todo-ai-chatbot"
branch: "main"
user: "user"
command: "/sp.constitution"
labels: ["constitution", "todo-ai-chatbot", "specification"]
links:
  spec: "null"
  ticket: "null"
  adr: "null"
  pr: "null"
files_yaml:
  - ".specify/memory/constitution.md"
tests_yaml: []
---

# Update Constitution for Todo AI Chatbot

## Summary

Updated the project constitution to reflect the detailed requirements for the Phase III Todo AI Chatbot project, incorporating all specifications including core principles, technology stack, architecture, database models, API specifications, MCP tools, and agent behavior rules.

## Outcome

The constitution file now contains comprehensive requirements for:
- Stateless server architecture
- OpenAI Agents SDK integration
- MCP-only task operations
- User experience and error handling
- Database models for Task, Conversation, and Message
- Chat API specification
- MCP tools specification (add_task, list_tasks, complete_task, delete_task, update_task)
- Agent behavior rules and natural language understanding examples

## Evaluation

The updated constitution aligns with all requirements specified in the user input, maintaining the project's focus on stateless architecture, MCP integration, and natural language task management.

PROMPT_TEXT: "# SP Constitution (Specification Constitution)\n\n## Project Title\n\n**Phase III: Todo AI Chatbot**\n\n## Purpose & Objective\n\nThe purpose of this specification is to define the complete functional, architectural, and behavioral requirements for building a **stateless, AI-powered Todo Chatbot** using **MCP (Model Context Protocol)** and the **OpenAI Agents SDK**.\n\nThe system must allow users to manage todo tasks through **natural language conversation**, while strictly following the **Agentic Dev Stack workflow**:\n\n> **Write Spec → Generate Plan → Break into Tasks → Implement via Claude Code**\n> ⚠️ **No manual coding is allowed.** Evaluation will be based on specs, prompts, iterations, and correctness.\n\n---\n\n## Development Principles (Constitution Rules)\n\n1. The server must be **stateless**.\n2. All conversation and task state must persist in the **database**.\n3. AI logic must be implemented using the **OpenAI Agents SDK only**.\n4. All task operations must be exposed via **MCP tools**.\n5. The AI Agent must never directly manipulate the database.\n6. MCP tools must be the **only interface** for task CRUD operations.\n7. Every user action must receive a **friendly confirmation response**.\n8. Errors must be handled gracefully and explained in natural language.\n\n---\n\n## Core Features (Basic Level)\n\n* Conversational interface for todo management\n* Natural language understanding for task actions\n* Persistent conversations with stateless API\n* MCP-based task tools\n* Resume conversations after server restart\n\n---\n\n## Technology Stack\n\n| Component      | Technology                 |\n| -------------- | -------------------------- |\n| Frontend       | OpenAI ChatKit             |\n| Backend        | Python FastAPI             |\n| AI Framework   | OpenAI Agents SDK          |\n| MCP Server     | Official MCP SDK           |\n| ORM            | SQLModel                   |\n| Database       | Neon Serverless PostgreSQL |\n| Authentication | Better Auth                |\n\n---\n\n## High-Level Architecture\n\n**Flow:**\nChatKit UI → FastAPI Chat Endpoint → OpenAI Agent → MCP Tools → Neon Database\n\n### Responsibilities\n\n* **Frontend:** Collect user input & display AI responses\n* **FastAPI Server:** Stateless request handling\n* **Agent:** Decision-making & tool selection\n* **MCP Server:** Task operations\n* **Database:** Persist tasks & conversations\n\n---\n\n## Database Models\n\n### Task\n\n| Field       | Description      |\n| ----------- | ---------------- |\n| id          | Primary key      |\n| user_id     | Owner of task    |\n| title       | Task title       |\n| description | Optional details |\n| completed   | Boolean status   |\n| created_at  | Creation time    |\n| updated_at  | Last update time |\n\n### Conversation\n\n| Field      | Description       |\n| ---------- | ----------------- |\n| id         | Conversation ID   |\n| user_id    | Owner             |\n| created_at | Start time        |\n| updated_at | Last message time |\n\n### Message\n\n| Field           | Description         |\n| --------------- | ------------------- |\n| id              | Message ID          |\n| user_id         | Owner               |\n| conversation_id | Linked conversation |\n| role            | user / assistant    |\n| content         | Message text        |\n| created_at      | Timestamp           |\n\n---\n\n## Chat API Specification\n\n### Endpoint\n\n`POST /api/{user_id}/chat`\n\n### Request Body\n\n| Field           | Required | Description                      |\n| --------------- | -------- | -------------------------------- |\n| conversation_id | No       | Existing conversation (optional) |\n| message         | Yes      | User natural language input      |\n\n### Response Body\n\n| Field           | Description            |\n| --------------- | ---------------------- |\n| conversation_id | Active conversation ID |\n| response        | Assistant reply        |\n| tool_calls      | MCP tools invoked      |\n\n---\n\n## MCP Tools Specification\n\n### Tool: add_task\n\n**Purpose:** Create a new task\n\n**Parameters:**\n\n* user_id (string, required)\n* title (string, required)\n* description (string, optional)\n\n**Returns:** task_id, status, title\n\n---\n\n### Tool: list_tasks\n\n**Purpose:** Retrieve tasks\n\n**Parameters:**\n\n* user_id (string, required)\n* status (optional: all | pending | completed)\n\n**Returns:** Array of task objects\n\n---\n\n### Tool: complete_task\n\n**Purpose:** Mark task as completed\n\n**Parameters:**\n\n* user_id (string, required)\n* task_id (integer, required)\n\n---\n\n### Tool: delete_task\n\n**Purpose:** Remove task\n\n**Parameters:**\n\n* user_id (string, required)\n* task_id (integer, required)\n\n---\n\n### Tool: update_task\n\n**Purpose:** Modify task\n\n**Parameters:**\n\n* user_id (string, required)\n* task_id (integer, required)\n* title (optional)\n* description (optional)\n\n---\n\n## Agent Behavior Rules\n\n| Scenario         | Agent Action            |\n| ---------------- | ----------------------- |\n| Add task         | Call add_task           |\n| List tasks       | Call list_tasks         |\n| Complete task    | Call complete_task      |\n| Delete task      | Call delete_task        |\n| Update task      | Call update_task        |\n| Ambiguous delete | List first, then delete |\n\nThe agent must:\n\n* Always confirm actions\n* Explain errors politely\n* Never expose internal system details\n\n---\n\n## Stateless Conversation Flow\n\n1. Receive user message\n2. Fetch conversation history from DB\n3. Append new user message\n4. Run agent with MCP tools\n5. Store assistant response\n6. Return response\n\n⚠️ No server memory between requests\n\n---\n\n## Natural Language Understanding Examples\n\n| User Input                    | Agent Tool               |\n| ----------------------------- | ------------------------ |\n| \"Add a task to buy groceries\" | add_task                 |\n| \"Show my tasks\"               | list_tasks               |\n| \"What's pending?\"             | list_tasks (pending)     |\n| \"Mark task 3 complete\"        | complete_task            |\n| \"Delete the meeting task\"     | list_tasks → delete_task |\n| \"Change task 1\"               | update_task              |\n\n---\n\n## Deliverables\n\n* GitHub Repository\n* /frontend (ChatKit UI)\n* /backend (FastAPI + Agents + MCP)\n* /specs (Agent & MCP specifications)\n* Database migrations\n* README (setup & usage)\n\n---\n\n## Success Criteria\n\n* Fully functional conversational todo chatbot\n* Stateless backend\n* Persistent conversations\n* Correct MCP tool usage\n* Clean confirmations & error handling\n\n---\n\n**This document is the single source of truth for implementation.**\nAny deviation is considered incorrect."

RESPONSE_TEXT: "Successfully updated the constitution file with all detailed requirements from the user input, including core principles, technology stack, architecture, database models, API specifications, MCP tools specifications, agent behavior rules, and natural language understanding examples."