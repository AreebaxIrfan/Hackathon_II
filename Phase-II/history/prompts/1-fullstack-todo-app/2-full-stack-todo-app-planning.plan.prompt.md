---
id: 2
title: "Full-Stack Todo App Planning"
stage: plan
date_iso: "2026-01-09"
surface: "agent"
model: "claude-sonnet-4-5-20250929"
feature: "1-fullstack-todo-app"
branch: "1-fullstack-todo-app"
user: "user"
command: "/sp.plan"
labels: ["planning", "architecture", "fullstack", "todo-app"]
links:
  spec: "specs/1-fullstack-todo-app/spec.md"
  plan: "specs/1-fullstack-todo-app/plan.md"
  ticket: null
  adr: null
  pr: null
files_yaml:
  - "specs/1-fullstack-todo-app/plan.md"
  - "specs/1-fullstack-todo-app/research.md"
  - "specs/1-fullstack-todo-app/data-model.md"
  - "specs/1-fullstack-todo-app/quickstart.md"
  - "specs/1-fullstack-todo-app/contracts/api-contract.md"
tests_yaml: []
---

# Full-Stack Todo App Planning

## Prompt Text

```
Phase II: Todo Full-Stack Web Application
Phase

phase2-web

Goal

Implement a secure, multi-user, full-stack Todo web application by transforming the Phase I console app into a modern web system using:

Spec-Kit Plus

Claude Code

Agentic Dev Stack workflow

This plan strictly follows:
spec → plan → tasks → implementation
❌ No manual coding

Inputs (Specs to Reference)

Claude Code must read and follow these specifications before implementation:

Core Specs

@specs/overview.md

@specs/features/task-crud.md

@specs/features/authentication.md

API & Data

@specs/api/rest-endpoints.md

@specs/database/schema.md

UI

@specs/ui/pages.md

@specs/ui/components.md

Guidance Files

/CLAUDE.md

/frontend/CLAUDE.md

/backend/CLAUDE.md

High-Level Execution Strategy

Establish monorepo + Spec-Kit context

Implement backend foundation (DB + API + JWT security)

Implement frontend foundation (Auth + API client)

Connect frontend and backend securely

Validate user isolation and persistence

Prepare system for Phase III extension

Implementation Plan
Step 1 — Repository & Spec Validation

Objective: Ensure Claude Code has full context

Verify .spec-kit/config.yaml structure

Confirm Phase II includes:

task-crud

authentication

Validate presence of required spec files

Ensure CLAUDE.md files exist at:

Root

/frontend

/backend

Outcome: Claude Code can navigate specs and repo correctly

Step 2 — Backend Foundation (FastAPI + SQLModel)

Objective: Prepare backend infrastructure

Initialize FastAPI app structure

Configure environment variables:

DATABASE_URL

BETTER_AUTH_SECRET

Create SQLModel engine and session handling

Implement database connection to Neon PostgreSQL

Specs Referenced

@specs/database/schema.md

/backend/CLAUDE.md

Step 3 — Authentication Verification Layer (JWT)

Objective: Secure backend APIs

Implement JWT verification dependency/middleware

Decode and validate JWT using shared secret

Extract authenticated user ID from token

Reject unauthorized requests with 401

Security Rules

Do not trust user_id from frontend

Enforce user ownership server-side

Specs Referenced

@specs/features/authentication.md

@specs/api/rest-endpoints.md

Step 4 — Task Data Models

Objective: Persist task data securely

Implement Task SQLModel

Associate tasks with authenticated user ID

Add indexes for:

user_id

completed

Specs Referenced

@specs/database/schema.md

@specs/features/task-crud.md

Step 5 — REST API Implementation

Objective: Implement required CRUD endpoints

Endpoints to implement:

GET /api/{user_id}/tasks

POST /api/{user_id}/tasks

GET /api/{user_id}/tasks/{id}

PUT /api/{user_id}/tasks/{id}

DELETE /api/{user_id}/tasks/{id}

PATCH /api/{user_id}/tasks/{id}/complete

Rules

All endpoints require JWT

Validate URL user_id matches JWT user

Filter all queries by authenticated user

Specs Referenced

@specs/api/rest-endpoints.md

@specs/features/task-crud.md

Step 6 — Frontend Authentication Setup (Next.js + Better Auth)

Objective: Enable user signup/signin

Configure Better Auth in Next.js

Enable JWT plugin

Ensure JWT is accessible for API calls

Store session securely

Specs Referenced

@specs/features/authentication.md

/frontend/CLAUDE.md

Step 7 — Frontend API Client

Objective: Secure communication with backend

Implement centralized API client (/lib/api.ts)

Attach JWT token to every request:

Authorization: Bearer <token>


Handle 401 Unauthorized gracefully

Specs Referenced

/frontend/CLAUDE.md

@specs/api/rest-endpoinud.md

Step 9 — End-to-End Integration

Objective: Validate full system behavior

User can sign up and log in

JWT is issued and attached to requests

Backend verifies token correctly

Tasks persist in Neon PostgreSQL

Users cannot access other users' tasks

Step 10 — Validation & Phase Completion

Objective: Confirm Phase II success

All Phase II success criteria met

No manual coding performed

Specs accurately reflect implementation

Codebase ready for Phase III (chatbot)

Deliverables

Secure FastAPI backend

Authenticated Next.js frontend

Persistent PostgreSQL database

Fully spec-driven monorepo

JWT-secured REST API

Multi-user task isolation

Exit Criteria (Phase II Complete)

✅ All 5 basic task features implemented

✅ Authentication enforced everywhere

✅ JWT verification works correctly

✅ Tasks persist across sessions

✅ Spec-first workflow demonstrated
```

## Response Text

Completed comprehensive planning for the Full-Stack Todo Web Application implementation. Created the following deliverables:

1. Implementation Plan (plan.md) - Technical architecture overview, project structure, and complexity tracking
2. Research Summary (research.md) - Technology decisions, API patterns, and security considerations
3. Data Model (data-model.md) - Entity definitions, relationships, validation rules, and business logic
4. Quickstart Guide (quickstart.md) - Setup instructions, environment configuration, and development workflow
5. API Contract (contracts/api-contract.md) - Complete API specification with endpoints, request/response formats, and error handling

The plan establishes a monorepo structure with separate backend (FastAPI) and frontend (Next.js) directories, implements JWT-based authentication with Better Auth, uses Neon Serverless PostgreSQL with SQLModel ORM for persistence, and ensures secure multi-user data isolation. All components follow the spec-driven development approach as required.