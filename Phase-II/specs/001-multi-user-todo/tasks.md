---
description: "Task list for Multi-user Todo Web Application"
---

# Tasks: Multi-user Todo Web Application

**Input**: Design documents from `/specs/001-multi-user-todo/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: The examples below include test tasks. Tests are OPTIONAL - only include them if explicitly requested in the feature specification.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Frontend**: `frontend/src/`, `frontend/tests/`
- **Backend**: `backend/src/`, `backend/tests/`
- Paths shown below follow the determined structure from plan.md

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [x] T001 Create project structure per implementation plan with frontend/ and backend/ directories
- [x] T002 Initialize frontend with Next.js 16+, TypeScript, Tailwind CSS
- [x] T003 Initialize backend with FastAPI, SQLModel, and Python 3.11+
- [x] T004 [P] Configure linting and formatting tools for both frontend and backend
- [x] T005 Create .env.example files for both frontend and backend with required variables

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

Examples of foundational tasks (adjust based on your project):

- [x] T006 Setup database schema and migrations framework in backend/src/db/
- [x] T007 [P] Install and configure Better Auth in frontend/
- [x] T008 [P] Setup JWT authentication middleware in backend/src/middleware/
- [x] T009 Create base Task model in backend/src/models/task.py
- [x] T010 Configure error handling and logging infrastructure in backend/src/utils/
- [x] T011 Setup environment configuration management in backend/src/config/

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - User Registration and Login (Priority: P1) 🎯 MVP

**Goal**: Enable new users to create accounts and authenticate to access their personal todo list

**Independent Test**: Can be fully tested by registering a new user account and successfully logging in with the provided credentials, then accessing the application.

### Tests for User Story 1 (OPTIONAL - only if tests requested) ⚠️

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [ ] T012 [P] [US1] Contract test for authentication endpoints in backend/tests/contract/test_auth.py
- [ ] T013 [P] [US1] Integration test for user registration flow in backend/tests/integration/test_registration.py

### Implementation for User Story 1

- [x] T014 [P] [US1] Create authentication API routes in backend/src/api/auth.py
- [x] T015 [P] [US1] Implement registration endpoint POST /auth/register in backend/src/api/auth.py
- [x] T016 [P] [US1] Implement login endpoint POST /auth/login in backend/src/api/auth.py
- [x] T017 [US1] Implement logout endpoint POST /auth/logout in backend/src/api/auth.py
- [x] T018 [US1] Create frontend authentication pages in frontend/src/app/signin/page.tsx
- [x] T019 [US1] Create frontend registration page in frontend/src/app/signup/page.tsx
- [x] T020 [US1] Implement authentication context/state management in frontend/src/context/auth.tsx

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently

---

## Phase 4: User Story 2 - Task Management Operations (Priority: P2)

**Goal**: Allow authenticated users to create, read, update, delete, and toggle completion status of their tasks

**Independent Test**: Can be fully tested by performing all five operations (create, read, update, delete, toggle completion) on tasks and verifying they work correctly for the authenticated user.

### Tests for User Story 2 (OPTIONAL - only if tests requested) ⚠️

- [ ] T021 [P] [US2] Contract test for task endpoints in backend/tests/contract/test_tasks.py
- [ ] T022 [P] [US2] Integration test for task CRUD flow in backend/tests/integration/test_task_crud.py

### Implementation for User Story 2

- [x] T023 [P] [US2] Create Task service in backend/src/services/task_service.py
- [x] T024 [US2] Implement GET /api/tasks endpoint in backend/src/api/tasks.py
- [x] T025 [US2] Implement POST /api/tasks endpoint in backend/src/api/tasks.py
- [x] T026 [US2] Implement GET /api/tasks/{task_id} endpoint in backend/src/api/tasks.py
- [x] T027 [US2] Implement PUT /api/tasks/{task_id} endpoint in backend/src/api/tasks.py
- [x] T028 [US2] Implement DELETE /api/tasks/{task_id} endpoint in backend/src/api/tasks.py
- [x] T029 [US2] Implement PATCH /api/tasks/{task_id}/complete endpoint in backend/src/api/tasks.py
- [x] T030 [US2] Create frontend task list page in frontend/src/app/dashboard/page.tsx
- [x] T031 [US2] Create task creation form component in frontend/src/components/task-form.tsx
- [x] T032 [US2] Create task list display component in frontend/src/components/task-list.tsx
- [x] T033 [US2] Create task completion toggle component in frontend/src/components/task-toggle.tsx

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently

---

## Phase 5: User Story 3 - Secure Data Isolation (Priority: P3)

**Goal**: Prevent users from accessing or modifying other users' tasks and enforce strong data isolation between users

**Independent Test**: Can be tested by attempting to access another user's tasks and verifying that unauthorized access is prevented with appropriate error responses.

### Tests for User Story 3 (OPTIONAL - only if tests requested) ⚠️

- [ ] T034 [P] [US3] Contract test for data isolation in backend/tests/contract/test_isolation.py
- [ ] T035 [P] [US3] Integration test for cross-user access prevention in backend/tests/integration/test_isolation.py

### Implementation for User Story 3

- [x] T036 [P] [US3] Create authentication dependency for protected endpoints in backend/src/api/deps.py
- [x] T037 [US3] Implement user ID extraction from JWT in backend/src/api/deps.py
- [x] T038 [US3] Add user ownership verification to all task endpoints in backend/src/api/tasks.py
- [x] T039 [US3] Add proper filtering by user_id in all task queries in backend/src/services/task_service.py
- [x] T040 [US3] Update frontend API client to include JWT in requests in frontend/src/lib/api-client.ts
- [x] T041 [US3] Add error handling for 401/403 responses in frontend/src/lib/api-client.ts

**Checkpoint**: All user stories should now be independently functional

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [x] T042 [P] Add loading states and error feedback to frontend components
- [x] T043 Add responsive mobile-first UI using Tailwind CSS classes
- [x] T044 Add proper error handling and validation across all endpoints
- [x] T045 [P] Documentation updates in docs/
- [x] T046 Code cleanup and refactoring
- [x] T047 Security hardening and validation
- [x] T048 Run quickstart.md validation

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3+)**: All depend on Foundational phase completion
  - User stories can then proceed in parallel (if staffed)
  - Or sequentially in priority order (P1 → P2 → P3)
- **Polish (Final Phase)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P2)**: Can start after Foundational (Phase 2) - May integrate with US1 but should be independently testable
- **User Story 3 (P3)**: Can start after Foundational (Phase 2) - May integrate with US1/US2 but should be independently testable

### Within Each User Story

- Tests (if included) MUST be written and FAIL before implementation
- Models before services
- Services before endpoints
- Core implementation before integration
- Story complete before moving to next priority

### Parallel Opportunities

- All Setup tasks marked [P] can run in parallel
- All Foundational tasks marked [P] can run in parallel (within Phase 2)
- Once Foundational phase completes, all user stories can start in parallel (if team capacity allows)
- All tests for a user story marked [P] can run in parallel
- Models within a story marked [P] can run in parallel
- Different user stories can be worked on in parallel by different team members

---

## Parallel Example: User Story 1

```bash
# Launch all tests for User Story 1 together (if tests requested):
Task: "Contract test for authentication endpoints in backend/tests/contract/test_auth.py"
Task: "Integration test for user registration flow in backend/tests/integration/test_registration.py"

# Launch all models for User Story 1 together:
Task: "Create authentication API routes in backend/src/api/auth.py"
Task: "Implement registration endpoint POST /auth/register in backend/src/api/auth.py"
Task: "Implement login endpoint POST /auth/login in backend/src/api/auth.py"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 3: User Story 1
4. **STOP and VALIDATE**: Test User Story 1 independently
5. Deploy/demo if ready

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 → Test independently → Deploy/Demo (MVP!)
3. Add User Story 2 → Test independently → Deploy/Demo
4. Add User Story 3 → Test independently → Deploy/Demo
5. Each story adds value without breaking previous stories

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together
2. Once Foundational is done:
   - Developer A: User Story 1
   - Developer B: User Story 2
   - Developer C: User Story 3
3. Stories complete and integrate independently

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Verify tests fail before implementing
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence