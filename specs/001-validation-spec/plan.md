# Implementation Plan: Frontend & Backend Validation

**Branch**: `001-validation-spec` | **Date**: 2026-02-05 | **Spec**: [D:/phase-three/specs/001-validation-spec/spec.md](file:///D:/phase-three/specs/001-validation-spec/spec.md)
**Input**: Feature specification from `/specs/001-validation-spec/spec.md`

## Summary

Implement and validate a fully functional Todo Full-Stack Application with a conversational AI interface, ensuring strict repository structure compliance and smooth frontend–backend integration. This includes moving frontend files from src/ to app/, implementing MCP server tools for Todo operations, integrating OpenAI Agents SDK for conversational interface, and ensuring all state is persisted in the database.

## Technical Context

**Language/Version**: TypeScript 5.0, Python 3.11
**Primary Dependencies**: Next.js 14, FastAPI, OpenAI Agents SDK, MCP SDK, SQLModel, Neon PostgreSQL
**Storage**: Neon PostgreSQL database with SQLModel ORM
**Testing**: Jest for frontend, pytest for backend
**Target Platform**: Web application with Node.js backend
**Project Type**: Web application with separate frontend and backend
**Performance Goals**: Sub-3 second response times for chat interactions, 95% uptime for core functionality
**Constraints**: Stateless architecture with database persistence, proper directory structure compliance
**Scale/Scope**: Single user focused initially, scalable to multiple users

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

All planned implementations align with project constitution, emphasizing clean architecture with separation of concerns between frontend and backend, proper state management through database persistence, and adherence to security best practices for authentication and authorization.

## Project Structure

### Documentation (this feature)

```text
specs/001-validation-spec/
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (/sp.plan command)
├── data-model.md        # Phase 1 output (/sp.plan command)
├── quickstart.md        # Phase 1 output (/sp.plan command)
├── contracts/           # Phase 1 output (/sp.plan command)
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)

```text
backend/
├── src/
│   ├── models/
│   ├── services/
│   ├── api/
│   ├── mcp/
│   └── agents/
└── tests/

frontend/
├── app/
│   ├── components/
│   ├── lib/
│   └── chat/
├── public/
└── tests/

specs/
└── 001-validation-spec/
    ├── spec.md
    ├── plan.md
    └── ...
```

**Structure Decision**: Selected web application structure with separate backend and frontend directories to maintain clear separation of concerns. Frontend code moved from src/ to app/ as required by specification.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|

## Phase 0: Outline & Research

### Research Tasks

1. **Directory Structure Investigation**
   - Audit current frontend/ directory structure
   - Identify all files in frontend/src/ that need relocation
   - Verify no backend code exists outside backend/ directory

2. **Next.js 14 App Router Implementation**
   - Research proper integration of chatbot UI component in Next.js 14
   - Investigate best practices for API communication between frontend and backend
   - Study error handling patterns for API calls

3. **MCP Server Implementation Research**
   - Investigate Official MCP SDK best practices
   - Study stateless tool design patterns for Todo operations
   - Research database integration patterns for persistent state

4. **OpenAI Agents SDK Integration**
   - Study OpenAI Agents SDK implementation patterns
   - Research conversation state management strategies
   - Investigate MCP tool calling mechanisms

5. **Database Schema Design**
   - Research optimal schema for Todos, Users, and Chat conversations
   - Study SQLModel best practices with Neon PostgreSQL
   - Investigate relationship patterns between entities

## Phase 1: Design & Contracts

### Data Model Design

**Todo Entity**:
- id: UUID
- title: String
- description: Text (optional)
- completed: Boolean
- user_id: UUID (foreign key)
- created_at: DateTime
- updated_at: DateTime

**User Entity**:
- id: UUID
- email: String (unique)
- username: String (unique)
- created_at: DateTime
- updated_at: DateTime

**ChatMessage Entity**:
- id: UUID
- conversation_id: UUID
- sender: String ('user' or 'assistant')
- content: Text
- timestamp: DateTime

**Conversation Entity**:
- id: UUID
- user_id: UUID (foreign key)
- created_at: DateTime
- updated_at: DateTime

### API Contracts

**Backend API Endpoints**:
- `POST /api/v1/chat/` - Process chat messages and route to AI agent
- `GET /api/v1/todos/` - Get user's todos
- `POST /api/v1/todos/` - Create new todo
- `PUT /api/v1/todos/{id}` - Update todo
- `DELETE /api/v1/todos/{id}` - Delete todo
- `POST /api/v1/auth/login` - User authentication
- `POST /api/v1/auth/logout` - User logout

**MCP Tool Contracts**:
- `todo.create(title: str, description: str, user_id: str)` → Todo object
- `todo.read(user_id: str, filters: dict)` → List[Todo]
- `todo.update(todo_id: str, updates: dict)` → Todo object
- `todo.delete(todo_id: str)` → Boolean
- `user.authenticate(credentials: dict)` → User object or None

### Quickstart Guide

1. Clone the repository
2. Install dependencies: `npm install` (frontend), `pip install -r requirements.txt` (backend)
3. Set up environment variables (database URL, API keys)
4. Run database migrations: `alembic upgrade head`
5. Start backend: `uvicorn backend.main:app --reload`
6. Start frontend: `npm run dev`
7. Access application at http://localhost:3000

### Agent Context Update

- Added MCP SDK integration patterns
- Included OpenAI Agents SDK usage guidelines
- Updated database schema design patterns
- Documented Next.js 14 App Router best practices