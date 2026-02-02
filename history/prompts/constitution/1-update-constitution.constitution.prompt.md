---
id: 1
title: Update Constitution
stage: constitution
date_iso: 2026-01-27
surface: agent
model: Claude Sonnet 4.5
feature: none
branch: main
user: user
command: /sp.constitution
labels: ["constitution", "todo-chatbot", "spec-driven"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files_yaml:
  - .specify/memory/constitution.md
tests_yaml: []
---

# Prompt History Record

## Original Prompt
```
/sp.constitution
Project

Todo Full-Stack Web Application (Phase II)
Transform the console-based todo app into a secure, multi-user, full-stack web application using a spec-driven, agentic development workflow.

Core Principles (5)

Spec-First Development
No implementation without a written and approved specification.

Agent-Driven Execution
All code is generated and modified exclusively via Claude Code using Spec-Kit Plus.

User Isolation by Design
Each user can only access and modify their own tasks at all times.

Stateless Backend Architecture
Backend services remain stateless; all state persists in the database.

Single Source of Truth
Specs in /specs directory are the authoritative reference for behavior and structure.

Key Standards (5)

RESTful API Compliance
All backend endpoints must follow REST conventions and return JSON responses.

JWT-Based Authentication
Every API request must be authenticated using JWT tokens issued by Better Auth.

Consistent Tech Stack Usage

Frontend: Next.js (App Router)

Backend: FastAPI + SQLModel

Database: Neon PostgreSQL

Responsive & Accessible UI
Frontend must be responsive and usable across devices.

Clear Spec Referencing
All implementations must explicitly reference relevant specs using @specs/....

Constraints (4)

No Manual Coding
Direct manual edits to code are not allowed.

No Auth Logic in Backend
Backend must only verify JWTs, not manage authentication sessions.

No Cross-User Data Access
Queries must always be filtered by authenticated user ID.

Monorepo Structure Mandatory
Frontend and backend must exist in a single repository with Spec-Kit structure.

Success Criteria (4)

Authenticated Multi-User Access
Users can sign up, sign in, and securely access their own tasks.

Fully Functional CRUD Operations
Tasks can be created, read, updated, deleted, and marked complete via the web UI.

Secure API Enforcement
Unauthorized requests receive 401 Unauthorized responses.

Spec-to-Code Traceability
Every major feature can be traced back to a written spec file.
```

## Response Summary
Updated the project constitution at `.specify/memory/constitution.md` to reflect the Todo AI Chatbot project requirements. The new constitution includes:

- Core Principles: Spec-First Development, Agent-Driven Execution, User Isolation by Design, Stateless Architecture, Single Source of Truth
- Technology Stack Requirements: OpenAI ChatKit, Python FastAPI, OpenAI Agents SDK, MCP SDK, SQLModel, Neon PostgreSQL, Better Auth
- Development Workflow: Agentic Dev Stack methodology with MCP architecture compliance
- Governance: Compliance requirements and amendment procedures

The constitution was updated from version 1.0.0 to 1.1.0 to reflect the transition from the Todo Full-Stack Web Application to the Todo AI Chatbot project with its specific MCP server architecture requirements.