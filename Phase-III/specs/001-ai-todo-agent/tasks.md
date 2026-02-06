---
description: "Task list for AI Todo Agent implementation"
---

# Tasks: AI Todo Agent with Natural Language Processing and MCP Tools

**Input**: Design documents from `/specs/001-ai-todo-agent/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: The examples below include test tasks. Tests are OPTIONAL - only include them if explicitly requested in the feature specification.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Backend**: `backend/src/`, `backend/tests/`
- **MCP Server**: `mcp-server/src/`, `mcp-server/tools/`
- **Frontend**: `frontend/src/`

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [X] T001 Create project structure with backend, mcp-server, and frontend directories
- [X] T002 Initialize Python project with FastAPI, SQLModel, OpenAI, and Better Auth dependencies in backend
- [X] T003 [P] Initialize Python project with MCP SDK dependencies in mcp-server
- [X] T004 [P] Configure linting and formatting tools for Python projects
- [X] T005 Set up environment configuration management with .env files

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [X] T006 Setup database schema and migrations framework using SQLModel in backend
- [ ] T007 [P] Implement authentication/authorization framework with Better Auth in backend
- [ ] T008 [P] Setup API routing and middleware structure in backend
- [ ] T009 Create base models/entities that all stories depend on in backend/src/models/
- [X] T010 Configure error handling and logging infrastructure in backend
- [X] T011 Setup MCP server framework and connection handling in mcp-server
- [X] T012 Create shared data models for tasks, conversations, and messages in backend/src/models/

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Natural Language Task Management (Priority: P1) 🎯 MVP

**Goal**: Enable users to interact with an AI-powered todo assistant using natural language to manage their tasks. The agent interprets the user's intent and performs the appropriate task operations using MCP tools, providing clear feedback on actions taken.

**Independent Test**: Can be fully tested by sending natural language commands to the agent (e.g., "Add a task to buy groceries", "Mark task 3 as complete") and verifying that the correct MCP tools are called and appropriate confirmations are provided.

### Tests for User Story 1 (OPTIONAL - only if tests requested) ⚠️

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [ ] T013 [P] [US1] Integration test for chat endpoint in backend/tests/integration/test_chat_endpoint.py
- [ ] T014 [P] [US1] Contract test for chat API in backend/tests/contract/test_chat_contract.py

### Implementation for User Story 1

- [X] T015 [P] [US1] Create Task model in backend/src/models/task.py
- [X] T016 [P] [US1] Create Conversation model in backend/src/models/conversation.py
- [X] T017 [P] [US1] Create Message model in backend/src/models/message.py
- [X] T018 [US1] Implement TaskService in backend/src/services/task_service.py
- [X] T019 [US1] Implement ConversationService in backend/src/services/conversation_service.py
- [X] T020 [US1] Implement add_task MCP tool in mcp-server/tools/task_operations.py
- [X] T021 [US1] Implement list_tasks MCP tool in mcp-server/tools/task_operations.py
- [X] T022 [US1] Implement complete_task MCP tool in mcp-server/tools/task_operations.py
- [X] T023 [US1] Implement delete_task MCP tool in mcp-server/tools/task_operations.py
- [X] T024 [US1] Implement update_task MCP tool in mcp-server/tools/task_operations.py
- [X] T025 [US1] Configure OpenAI Agent to use MCP tools in backend/src/agents/todo_agent.py
- [X] T026 [US1] Implement chat endpoint in backend/src/api/v1/chat.py
- [X] T027 [US1] Add validation and error handling for user story 1
- [X] T028 [US1] Add logging for user story 1 operations
- [X] T029 [US1] Implement user isolation logic to ensure proper access control

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently

---

## Phase 4: User Story 2 - Ambiguous Task Reference Resolution (Priority: P2)

**Goal**: When a user makes a request that could refer to multiple tasks or an unclear task, the agent intelligently resolves the ambiguity by listing relevant tasks first before performing the requested action.

**Independent Test**: Can be fully tested by providing ambiguous requests (e.g., "Delete the meeting task" when multiple meeting tasks exist) and verifying that the agent lists tasks first before asking for clarification.

### Tests for User Story 2 (OPTIONAL - only if tests requested) ⚠️

- [ ] T030 [P] [US2] Integration test for ambiguous task resolution in backend/tests/integration/test_ambiguous_resolution.py
- [ ] T031 [P] [US2] Contract test for ambiguous task handling in backend/tests/contract/test_ambiguous_contract.py

### Implementation for User Story 2

- [ ] T032 [P] [US2] Enhance TaskService with search and filtering capabilities in backend/src/services/task_service.py
- [ ] T033 [US2] Update OpenAI Agent to detect ambiguous references in backend/src/agents/todo_agent.py
- [ ] T034 [US2] Implement logic to list tasks before performing ambiguous actions in backend/src/agents/todo_agent.py
- [ ] T035 [US2] Add improved natural language processing for ambiguity detection in backend/src/agents/todo_agent.py
- [ ] T036 [US2] Integrate with User Story 1 components for enhanced task management

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently

---

## Phase 5: User Story 3 - Error Handling and Polite Feedback (Priority: P3)

**Goal**: When the system encounters errors or the user provides unclear input, the agent responds with polite, user-friendly messages that don't expose internal system details.

**Independent Test**: Can be fully tested by providing invalid commands or causing errors and verifying that the agent responds appropriately without revealing system internals.

### Tests for User Story 3 (OPTIONAL - only if tests requested) ⚠️

- [ ] T037 [P] [US3] Integration test for error handling in backend/tests/integration/test_error_handling.py
- [ ] T038 [P] [US3] Contract test for error responses in backend/tests/contract/test_error_contract.py

### Implementation for User Story 3

- [ ] T039 [P] [US3] Implement comprehensive error handling middleware in backend/src/middleware/error_handler.py
- [ ] T040 [US3] Update OpenAI Agent to provide polite error messages in backend/src/agents/todo_agent.py
- [ ] T041 [US3] Implement fallback responses for unrecognized user input in backend/src/agents/todo_agent.py
- [ ] T042 [US3] Add system isolation logic to prevent exposing internal details in backend/src/agents/todo_agent.py
- [ ] T043 [US3] Enhance confirmation messages with proper styling (e.g., "✅", "🗑️") in backend/src/agents/todo_agent.py

**Checkpoint**: All user stories should now be independently functional

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [ ] T044 [P] Documentation updates in docs/
- [ ] T045 Code cleanup and refactoring across all components
- [ ] T046 Performance optimization across all stories
- [ ] T047 [P] Additional unit tests (if requested) in backend/tests/unit/
- [ ] T048 Security hardening for user isolation and data protection
- [ ] T049 Run quickstart.md validation to ensure setup instructions work
- [ ] T050 Frontend integration with ChatKit UI in frontend/src/pages/chat.jsx

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
- **User Story 2 (P2)**: Can start after Foundational (Phase 2) - Builds upon US1 components but should be independently testable
- **User Story 3 (P3)**: Can start after Foundational (Phase 2) - May enhance US1/US2 but should be independently testable

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
# Launch all models for User Story 1 together:
Task: "Create Task model in backend/src/models/task.py"
Task: "Create Conversation model in backend/src/models/conversation.py"
Task: "Create Message model in backend/src/models/message.py"

# Launch all MCP tools for User Story 1 together:
Task: "Implement add_task MCP tool in mcp-server/tools/task_operations.py"
Task: "Implement list_tasks MCP tool in mcp-server/tools/task_operations.py"
Task: "Implement complete_task MCP tool in mcp-server/tools/task_operations.py"
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