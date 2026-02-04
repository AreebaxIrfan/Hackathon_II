# Implementation Plan: AI Todo Agent with Natural Language Processing and MCP Tools

**Feature**: 001-ai-todo-agent
**Created**: 2026-02-04
**Status**: Draft
**Author**: Claude

## Technical Context

### Architecture Overview
The AI Todo Agent will be implemented as a stateless service that integrates with the OpenAI Agents SDK and MCP tools to provide natural language task management. The architecture follows the flow: ChatKit UI → FastAPI Chat Endpoint → OpenAI Agent → MCP Tools → Neon Database.

### Technology Stack
- **Frontend**: OpenAI ChatKit
- **Backend**: Python FastAPI
- **AI Framework**: OpenAI Agents SDK
- **MCP Server**: Official MCP SDK
- **ORM**: SQLModel
- **Database**: Neon Serverless PostgreSQL
- **Authentication**: Better Auth

### Data Models
- **Task**: id, user_id, title, description, completed, created_at, updated_at
- **Conversation**: id, user_id, created_at, updated_at
- **Message**: id, user_id, conversation_id, role, content, created_at

### Current Unknowns
- [NEEDS CLARIFICATION: Specific OpenAI model to use for the agent]
- [NEEDS CLARIFICATION: MCP server configuration and hosting approach]
- [NEEDS CLARIFICATION: Authentication flow between frontend and backend]

## Constitution Check

### Compliance Verification
- ✅ **Stateless Server Architecture**: Chat endpoint will be stateless, retrieving conversation history from DB for each request
- ✅ **AI Logic via OpenAI Agents SDK**: Will implement using OpenAI Agents SDK only
- ✅ **MCP-Only Task Operations**: All task operations will be exposed via MCP tools
- ✅ **User Experience and Error Handling**: Will provide friendly confirmations and handle errors gracefully
- ✅ **User Isolation by Design**: Database queries will be filtered by authenticated user ID
- ✅ **Single Source of Truth**: Following the spec in specs/001-ai-todo-agent/spec.md

### Gate Evaluation
All constitutional requirements are satisfied by the planned implementation approach.

## Phase 0: Research & Discovery

### Research Areas
1. **OpenAI Agent Configuration**: Determine the best approach for integrating with the OpenAI Agents SDK for natural language processing
2. **MCP Tool Implementation**: Research best practices for implementing MCP tools that interact with the database
3. **Authentication Flow**: Investigate the Better Auth integration with both frontend and backend
4. **Stateless Conversation Management**: Research patterns for maintaining conversation statelessness while preserving context

### Expected Outcomes
- Decision on specific OpenAI model and agent configuration
- MCP server setup approach and tool definitions
- Authentication flow between components
- Conversation persistence strategy

## Phase 1: Design & Contracts

### Data Model Design
#### Task Entity
- **Fields**: id (int, PK), user_id (string), title (string), description (string, nullable), completed (bool), created_at (datetime), updated_at (datetime)
- **Validation**: Title is required, user_id must match authenticated user
- **Relationships**: Belongs to User, linked to Conversation through Messages

#### Conversation Entity
- **Fields**: id (int, PK), user_id (string), created_at (datetime), updated_at (datetime)
- **Validation**: user_id must match authenticated user
- **Relationships**: Has many Messages

#### Message Entity
- **Fields**: id (int, PK), user_id (string), conversation_id (int), role (string), content (string), created_at (datetime)
- **Validation**: Role must be 'user' or 'assistant', user_id must match authenticated user
- **Relationships**: Belongs to Conversation

### API Contract Design
#### Chat Endpoint
- **Path**: POST `/api/{user_id}/chat`
- **Request Body**:
  - `conversation_id` (optional string): Existing conversation ID
  - `message` (required string): User's natural language input
- **Response Body**:
  - `conversation_id` (string): Active conversation ID
  - `response` (string): Assistant's reply
  - `tool_calls` (array): MCP tools invoked

### MCP Tool Contracts
#### add_task
- **Purpose**: Create a new task
- **Parameters**:
  - `user_id` (required string)
  - `title` (required string)
  - `description` (optional string)
- **Returns**: `task_id`, `status`, `title`

#### list_tasks
- **Purpose**: Retrieve tasks
- **Parameters**:
  - `user_id` (required string)
  - `status` (optional string: all|pending|completed)
- **Returns**: Array of task objects

#### complete_task
- **Purpose**: Mark task as completed
- **Parameters**:
  - `user_id` (required string)
  - `task_id` (required integer)
- **Returns**: Success status

#### delete_task
- **Purpose**: Remove task
- **Parameters**:
  - `user_id` (required string)
  - `task_id` (required integer)
- **Returns**: Success status

#### update_task
- **Purpose**: Modify task
- **Parameters**:
  - `user_id` (required string)
  - `task_id` (required integer)
  - `title` (optional string)
  - `description` (optional string)
- **Returns**: Success status

### Quickstart Guide
1. Set up environment variables (database URL, auth secrets, OpenAI API key)
2. Run database migrations
3. Start MCP server
4. Start FastAPI backend
5. Run frontend

## Phase 2: Implementation Approach

### Component Breakdown
1. **MCP Tools Layer**: Implement database operations as MCP tools
2. **AI Agent Layer**: Configure OpenAI Agent to use MCP tools
3. **API Layer**: Create stateless chat endpoint
4. **Authentication Layer**: Integrate Better Auth
5. **Frontend Integration**: Connect ChatKit to backend

### Development Sequence
1. MCP Tools Implementation
2. Database Models & Migrations
3. FastAPI Backend with Chat Endpoint
4. OpenAI Agent Configuration
5. Frontend Integration
6. Authentication Setup
7. Testing & Validation

### Risk Mitigation
- **Natural Language Understanding**: Extensive testing with various user inputs
- **Statelessness**: Proper conversation history retrieval and storage
- **Security**: Proper user isolation and authentication
- **Performance**: Efficient database queries and caching strategies

## Phase 3: Validation & Testing

### Unit Tests
- MCP tool functionality
- Data model validation
- API endpoint behavior
- Authentication middleware

### Integration Tests
- End-to-end conversation flow
- Natural language processing accuracy
- Database operation integrity
- Authentication flow

### Acceptance Criteria
- All acceptance scenarios from spec are satisfied
- Natural language processing achieves 90% accuracy
- Response time under 3 seconds for 95% of interactions
- Proper handling of ambiguous references
- Graceful error handling without exposing system details