# REST API Endpoints Specification

## Overview
Secure, RESTful API endpoints for task management with JWT-based authentication.

## Requirements
- All task-related endpoints must follow REST conventions
- Every API request requires a valid JWT token
- Endpoints return correct HTTP status codes and JSON responses
- API only exposes tasks belonging to the authenticated user
- All routes must be prefixed with /api/
- Backend must only verify JWT, not manage auth sessions
- User identity must be derived from JWT, not request body
- API must be implemented using FastAPI conventions

## Functional Requirements
1. Create new tasks
2. Retrieve user's tasks
3. Update existing tasks
4. Delete tasks
5. Complete/incomplete tasks

## Non-functional Requirements
- Authentication: JWT-based
- Authorization: User isolation (can only access own tasks)
- Response format: JSON
- Status codes: Standard HTTP codes