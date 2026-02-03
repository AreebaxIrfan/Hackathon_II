<!--
Sync Impact Report:
Version change: 1.0.0 → 1.1.0
Modified principles: None (completely new constitution)
Added sections: All sections updated with Todo AI Chatbot specific content
Removed sections: None (first version)
Templates requiring updates: ⚠ pending - .specify/templates/plan-template.md, .specify/templates/spec-template.md, .specify/templates/tasks-template.md
Follow-up TODOs: None
-->
# Todo AI Chatbot Constitution

## Core Principles

### Spec-First Development
No implementation without a written and approved specification. All features and changes must be documented in spec files before any code is written.

### Agent-Driven Execution
All code is generated and modified exclusively via Claude Code using Spec-Kit Plus. No manual coding is allowed - all development must follow the Agentic Dev Stack workflow: Write spec → Generate plan → Break into tasks → Implement via Claude Code.

### User Isolation by Design
Each user can only access and modify their own tasks at all times. Database queries must always be filtered by authenticated user ID to prevent cross-user data access.

### Stateless Architecture
Backend services and MCP tools remain stateless; all state persists in the database. The chat endpoint is stateless and retrieves conversation history from the database for each request.

### Single Source of Truth
Specs in /specs directory are the authoritative reference for behavior and structure. All implementations must explicitly reference relevant specs using @specs/....

## Technology Stack Requirements

- Frontend: OpenAI ChatKit
- Backend: Python FastAPI
- AI Framework: OpenAI Agents SDK
- MCP Server: Official MCP SDK
- ORM: SQLModel
- Database: Neon Serverless PostgreSQL
- Authentication: Better Auth
- All components must integrate seamlessly with the MCP (Model Context Protocol) architecture

## Development Workflow

- Use the Agentic Dev Stack workflow: Write spec → Generate plan → Break into tasks → Implement via Claude Code
- MCP tools must be implemented following the official MCP SDK specifications
- Database models must follow SQLModel conventions with proper relationships
- All API endpoints must follow REST conventions and properly handle JWT authentication
- AI agent behavior must follow the specified natural language command mappings
- Conversation flow must maintain statelessness while preserving context via database

## Governance

This constitution governs all development activities for the Todo AI Chatbot project. All code changes, architectural decisions, and feature implementations must comply with these principles. Amendments to this constitution require explicit approval and must be documented with versioning. Development teams must verify compliance with all principles during code reviews and testing phases.

**Version**: 1.1.0 | **Ratified**: 2026-01-27 | **Last Amended**: 2026-01-27
