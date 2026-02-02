<!-- Sync Impact Report:
- Version change: 1.0.0 → 1.1.0 (minor update with governance refinement and tech stack alignment)
- Modified principles: Updated Technology Constitution and Authentication Architecture Principles to reflect 2026 best practices
- Added sections: None
- Removed sections: None
- Templates requiring updates: ✅ Updated
- Follow-up TODOs: None
-->
# hackathon-todo Constitution

## Core Principles

### Project Identity & Purpose
Phase: II – Full-Stack Web Application (Basic Level), Ultimate Goal: Transform console-based todo → secure multi-user web app with persistent storage, Core Purpose: Demonstrate clean spec-driven, agentic full-stack development using Claude Code + Spec-Kit Plus workflow with 2026 technology stack

### Non-Negotiable Requirements
1. Multi-user application with strong user data isolation - each user sees only their own tasks
2. Persistent storage in Neon Serverless PostgreSQL with proper connection management
3. Complete Task CRUD (Create, Read, Update, Delete) + toggle complete functionality
4. Responsive, clean UI with mobile-first design approach using Tailwind CSS
5. Authentication via Better Auth (email/password + optional social login)
6. JWT-based stateless authentication between Next.js ↔ FastAPI with proper middleware
7. REST API secured properly with user ownership verification
8. Strict spec-driven development (no manual coding, only spec-driven workflow)

### Technology Constitution (2026 Edition Locked Stack)
Frontend: Next.js 16+ (App Router) with TypeScript + Tailwind CSS, Backend: Python FastAPI (Latest stable) with modern async style, ORM/Models: SQLModel (compatible with Pydantic v2), Database: Neon Serverless PostgreSQL with DATABASE_URL env var, Authentication: Better Auth (latest ~1.4+) with JWT plugin for external API, Spec & Agent system: Claude Code + Spec-Kit Plus, Project Structure: Mandatory Monorepo

### Sacred API Contract
RESTful + user_id in path for explicit ownership, Endpoints: GET /api/{user_id}/tasks (List tasks), POST /api/{user_id}/tasks (Create task), GET /api/{user_id}/tasks/{id} (Get single task), PUT /api/{user_id}/tasks/{id} (Full update task), DELETE /api/{user_id}/tasks/{id} (Delete task), PATCH /api/{user_id}/tasks/{id}/complete (Toggle completion status), Security: Every endpoint requires valid JWT, 401 Unauthorized for missing/invalid token, 403 Forbidden for authenticated but not owner, Backend filters by authenticated user_id

### Authentication Architecture Principles (2026 Best Practice)
Better Auth operates in Next.js frontend layer, JWT tokens issued on successful login/signup, Same BETTER_AUTH_SECRET configured in both frontend & backend services, FastAPI implements middleware that verifies signature, extracts user identity, enforces ownership on every operation, Stateless architecture - no sessions in backend, no database lookup for auth validation, Modern approach avoids simple symmetric secret + JWT plugin pattern of older guides

### Core Project Values & Laws
Law #1 – Spec-Driven Development: No implementation without spec, Law #2 – Agent-First: Use Claude Code + Spec-Kit Plus for all dev tasks, Law #3 – Minimalism: Smallest viable changes, no feature creep, Law #4 – Traceability: Every change has clear justification, Law #5 – Quality Gates: All code passes tests, follows standards, Law #6 – Compliance: Every feature must adhere to constitution principles

## Canonical Folder Constitution
Required folder structure: hackathon-todo/ with .specify/, specs/, frontend/, backend/, and essential configuration files following monorepo pattern

## Current Phase Scope Declaration
Phase II Basic Level ends when: Clean user signup & signin flows (email/password + optional social), Strong user data isolation with each user seeing only their tasks, All 6 REST endpoints implemented & secured with proper authentication, Full task CRUD + complete toggle working for multiple users, Responsive mobile-first UI with clean design, Data persistently stored in Neon PostgreSQL, Clear, up-to-date specifications covering all above points, All functionality delivered through spec-driven agentic workflow only

## Governance
May the specs be precise, the agents diligent, and the code clean. — Constitution of hackathon-todo Phase II Effective January 2026

**Version**: 1.1.0 | **Ratified**: 2026-01-11 | **Last Amended**: 2026-01-11