# Implementation Plan: Chat Flow & API for Stateless Todo Assistant

**Feature**: 001-chat-flow-api
**Created**: 2026-02-04
**Status**: Draft
**Author**: Claude

## Technical Context

### Architecture Overview
The chat API will be implemented as a stateless FastAPI endpoint that integrates with the OpenAI Agent and MCP tools. The architecture follows the flow: ChatKit UI → FastAPI Chat Endpoint → OpenAI Agent → MCP Tools → Database. The system ensures conversation persistence through database storage while maintaining a stateless server architecture.

### Technology Stack
- **Framework**: FastAPI
- **AI Framework**: OpenAI Agents SDK
- **MCP Server**: Official MCP SDK
- **ORM**: SQLModel
- **Database**: PostgreSQL (Neon Serverless)
- **Frontend**: OpenAI ChatKit

### Data Models
- **Conversation**: id, user_id, created_at, updated_at
- **Message**: id, user_id, conversation_id, role, content, created_at
- **ToolCall**: id, conversation_id, tool_name, arguments, result, created_at

### Current Unknowns
- [NEEDS CLARIFICATION: Specific OpenAI model to use for the agent]
- [NEEDS CLARIFICATION: Conversation ID generation strategy]
- [NEEDS CLARIFICATION: Error handling approach for MCP tool failures]

## Constitution Check

### Compliance Verification
- ✅ **Stateless Server Architecture**: Chat endpoint will be stateless, retrieving conversation history from DB for each request
- ✅ **AI Logic via OpenAI Agents SDK**: Will implement using OpenAI Agents SDK only
- ✅ **MCP-Only Task Operations**: All task operations will be handled via MCP tools
- ✅ **User Experience and Error Handling**: Will provide friendly confirmations and handle errors gracefully
- ✅ **User Isolation by Design**: Database queries will be filtered by authenticated user_id
- ✅ **Single Source of Truth**: Following the spec in specs/001-chat-flow-api/spec.md

### Gate Evaluation
All constitutional requirements are satisfied by the planned implementation approach.

## Phase 0: Research & Discovery

### Research Areas
1. **OpenAI Agent Configuration**: Determine the best approach for integrating with the OpenAI Agents SDK for chat processing
2. **Conversation Management**: Research patterns for managing conversation state in a stateless architecture
3. **Error Handling**: Study approaches for handling MCP tool failures gracefully
4. **Performance Optimization**: Investigate strategies for efficient conversation history retrieval

### Expected Outcomes
- Decision on specific OpenAI model and agent configuration
- Conversation ID generation approach
- Error handling strategy for tool failures
- Performance optimization techniques

## Phase 1: Design & Contracts

### Data Model Design
#### Conversation Entity
- **Fields**: id (int, PK), user_id (string), created_at (datetime), updated_at (datetime)
- **Validation**: user_id must match authenticated user
- **Relationships**: Has many Messages

#### Message Entity
- **Fields**: id (int, PK), user_id (string), conversation_id (int), role (string), content (string), created_at (datetime)
- **Validation**: Role must be 'user' or 'assistant', user_id must match authenticated user
- **Relationships**: Belongs to Conversation

#### ToolCall Entity
- **Fields**: id (int, PK), conversation_id (int), tool_name (string), arguments (JSON), result (JSON), created_at (datetime)
- **Validation**: conversation_id must exist, tool_name must be valid
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

### Quickstart Guide
1. Set up environment variables (database URL, OpenAI API key)
2. Run database migrations
3. Start FastAPI server
4. Connect ChatKit UI to the API

## Phase 2: Implementation Approach

### Component Breakdown
1. **Database Layer**: SQLModel models and database connection
2. **Service Layer**: Conversation and message management services
3. **AI Agent Layer**: OpenAI Agent configuration with MCP tool integration
4. **API Layer**: FastAPI endpoint with proper request/response handling
5. **Error Handling**: Comprehensive error handling and logging

### Development Sequence
1. Database Models & Connection Setup
2. Service Layer Implementation
3. OpenAI Agent Configuration
4. API Endpoint Implementation
5. Error Handling & Logging
6. Testing & Validation

### Risk Mitigation
- **Statelessness**: Proper conversation history retrieval for each request
- **Security**: User isolation through user_id validation
- **Performance**: Efficient database queries and indexing
- **Reliability**: Graceful handling of MCP tool failures

## Phase 3: Validation & Testing

### Unit Tests
- API endpoint functionality
- Data model validation
- Service layer operations
- Error handling

### Integration Tests
- End-to-end chat flow
- Conversation persistence
- MCP tool integration
- User isolation

### Acceptance Criteria
- All acceptance scenarios from spec are satisfied
- Stateless architecture functions properly
- User isolation maintained across all operations
- Error conditions handled gracefully