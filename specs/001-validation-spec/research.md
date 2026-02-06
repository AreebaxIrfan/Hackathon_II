# Research: Frontend & Backend Validation Implementation

**Feature**: 001-validation-spec
**Date**: 2026-02-05

## Directory Structure Investigation

### Current State Assessment
- **Issue**: Need to audit current frontend/ directory structure
- **Action**: Identify all files in frontend/src/ that need relocation
- **Result**: All frontend files must be moved from frontend/src/ to frontend/app/

### Backend Structure Validation
- **Issue**: Verify no backend code exists outside backend/ directory
- **Action**: Audit entire repository for misplaced backend code
- **Result**: All backend logic must be confined to backend/ directory

## Next.js 14 App Router Implementation

### Chatbot UI Integration
- **Decision**: Use OpenAI ChatKit UI or custom implementation with React components
- **Rationale**: OpenAI ChatKit provides robust chat interface with built-in features, while custom implementation offers more control
- **Alternative**: Custom React chat component with WebSocket support
- **Chosen**: Custom implementation for better integration with Todo functionality

### API Communication Patterns
- **Decision**: Use fetch API with proper error handling for frontend-backend communication
- **Rationale**: Next.js 14 provides excellent support for API routes and external API calls
- **Alternatives**: Axios, SWR, React Query
- **Chosen**: Native fetch with React Query for caching and state management

### Error Handling Best Practices
- **Decision**: Implement centralized error handling with user-friendly messages
- **Rationale**: Consistent error handling improves user experience
- **Approach**: Create error boundary components and API response interceptors

## MCP Server Implementation

### MCP SDK Integration
- **Decision**: Use Official MCP SDK for tool definition and registration
- **Rationale**: Official SDK provides standardized approach for MCP tools
- **Pattern**: Stateless tools that delegate to database services
- **Reference**: MCP specification for tool definition and execution

### Stateless Tool Design
- **Decision**: Design all MCP tools to be stateless with database persistence
- **Rationale**: Stateless tools are more reliable and easier to scale
- **Implementation**: Tools accept all necessary parameters, return results, persist state in DB
- **Best Practice**: Use transactional patterns for complex operations

## OpenAI Agents SDK Integration

### Agent Configuration
- **Decision**: Use OpenAI Assistant API with function calling for MCP integration
- **Rationale**: Function calling allows direct integration with MCP tools
- **Setup**: Define tools as functions, register with Assistant, process responses
- **State Management**: Conversation state persisted in database, not in agent

### Conversation Flow
- **Decision**: Implement stateless chat endpoint with database-backed conversation history
- **Rationale**: Maintains consistency with stateless architecture requirement
- **Process**: Receive message → Create/run Assistant → Save thread to DB → Return response
- **Integration**: MCP tools called as functions within Assistant execution

## Database Schema Design

### SQLModel Best Practices
- **Decision**: Use SQLModel for database models with Pydantic compatibility
- **Rationale**: Combines SQLAlchemy power with Pydantic validation
- **Structure**: Base model with common fields, specific models extending base
- **Relationships**: Proper foreign key constraints and relationship definitions

### Entity Relationships
- **Decision**: Todos belong to Users, ChatMessages belong to Conversations
- **Rationale**: Clear ownership model for data isolation and security
- **Access Control**: Always filter by user_id for proper authorization
- **Indexing**: Optimize frequently queried fields (user_id, timestamps)

## Authentication & Authorization

### Security Approach
- **Decision**: Implement JWT-based authentication with secure token handling
- **Rationale**: JWT tokens provide stateless authentication suitable for API
- **Implementation**: Token generation/verification in backend, storage in frontend
- **Security**: Secure cookie storage with HttpOnly flag or secure localStorage alternative

## Alternatives Considered

### Frontend Framework Alternatives
- **Option A**: Next.js 14 App Router (selected)
  - Pros: Excellent SSR/SSG support, rich ecosystem, good for full-stack apps
  - Cons: Learning curve for new developers
- **Option B**: React + Vite
  - Pros: Faster builds, simpler setup
  - Cons: Less integrated solution for full-stack applications

### Backend Framework Alternatives
- **Option A**: FastAPI (selected)
  - Pros: Automatic API documentation, async support, Pydantic integration
  - Cons: Newer framework, smaller ecosystem than Flask
- **Option B**: Django
  - Pros: Mature framework, built-in admin panel
  - Cons: Heavier framework, more opinionated structure

### Database Integration Alternatives
- **Option A**: SQLModel + Neon PostgreSQL (selected)
  - Pros: Combines Pydantic validation with SQLAlchemy power, serverless PostgreSQL
  - Cons: Newer combination, less community examples
- **Option B**: SQLAlchemy + PostgreSQL
  - Pros: Mature ORM, extensive documentation
  - Cons: Missing Pydantic integration benefits

### AI Integration Alternatives
- **Option A**: OpenAI Agents SDK + MCP (selected)
  - Pros: Standardized approach, extensible tool system, proper integration patterns
  - Cons: More complex setup than direct API calls
- **Option B**: Direct OpenAI API calls
  - Pros: Simpler setup, more control over requests
  - Cons: Less structured approach to tool integration