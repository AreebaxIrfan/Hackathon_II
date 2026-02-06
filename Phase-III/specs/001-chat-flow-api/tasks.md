---
description: "Task list for Chat Flow & API implementation"
---

# Tasks: Chat Flow & API for Stateless Todo Assistant

**Input**: Design documents from `/specs/001-chat-flow-api/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: The examples below include test tasks. Tests are OPTIONAL - only include them if explicitly requested in the feature specification.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Backend**: `backend/src/`, `backend/tests/`
- **API**: `backend/src/api/`
- **Services**: `backend/src/services/`
- **Models**: `backend/src/models/`
- **Agents**: `backend/src/agents/`

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [X] T001 Create project structure with backend directory
- [X] T002 Initialize Python project with FastAPI, SQLModel, OpenAI, and MCP SDK dependencies in backend
- [X] T003 [P] Configure linting and formatting tools for Python project

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [ ] T004 Setup database schema and migrations framework using SQLModel in backend
- [X] T005 [P] Create Conversation model in backend/src/models/conversation.py
- [X] T006 [P] Create Message model in backend/src/models/message.py
- [X] T007 [P] Create ToolCall model in backend/src/models/tool_call.py
- [X] T008 Create database connection and session management in backend/src/database.py
- [X] T009 Create ConversationService in backend/src/services/conversation_service.py
- [X] T010 Setup environment configuration management with .env files

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Send Natural Language Message to Todo Assistant (Priority: P1) 🎯 MVP

**Goal**: Enable users to send natural language messages to the AI-powered todo assistant through the chat API, with the system processing the message, storing it in the database, running the AI agent with MCP tools to generate a response, storing the response, and returning it to the user.

**Independent Test**: Can be fully tested by sending a message to the API endpoint and verifying that a response is received with appropriate tool calls based on the natural language input.

### Tests for User Story 1 (OPTIONAL - only if tests requested) ⚠️

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [ ] T011 [P] [US1] Integration test for chat endpoint in backend/tests/integration/test_chat_endpoint.py
- [ ] T012 [P] [US1] Contract test for chat API in backend/tests/contract/test_chat_contract.py

### Implementation for User Story 1

- [X] T013 [US1] Implement OpenAI Agent with MCP tools integration in backend/src/agents/todo_agent.py
- [X] T014 [US1] Implement chat endpoint in backend/src/api/v1/chat.py
- [X] T015 [US1] Add conversation history retrieval to chat endpoint in backend/src/api/v1/chat.py
- [X] T016 [US1] Add user message storage to chat endpoint in backend/src/api/v1/chat.py
- [X] T017 [US1] Add AI response storage to chat endpoint in backend/src/api/v1/chat.py
- [X] T018 [US1] Add validation and error handling for user story 1
- [X] T019 [US1] Add logging for user story 1 operations

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently

---

## Phase 4: User Story 2 - Maintain Conversation Context Across Requests (Priority: P2)

**Goal**: Enable the system to maintain context by fetching historical messages from the database for each request, ensuring continuity despite the stateless architecture when users engage in multi-turn conversations with the AI assistant.

**Independent Test**: Can be fully tested by sending multiple messages in sequence and verifying that the AI assistant demonstrates awareness of previous exchanges in the conversation.

### Tests for User Story 2 (OPTIONAL - only if tests requested) ⚠️

- [ ] T020 [P] [US2] Integration test for conversation context maintenance in backend/tests/integration/test_conversation_context.py
- [ ] T021 [P] [US2] Contract test for conversation context handling in backend/tests/contract/test_conversation_contract.py

### Implementation for User Story 2

- [ ] T022 [US2] Enhance ConversationService with message history retrieval in backend/src/services/conversation_service.py
- [ ] T023 [US2] Update OpenAI Agent to use conversation history in backend/src/agents/todo_agent.py
- [ ] T024 [US2] Add context-aware processing to chat endpoint in backend/src/api/v1/chat.py
- [ ] T025 [US2] Add server restart resilience to conversation handling
- [ ] T026 [US2] Integrate with User Story 1 components for enhanced functionality

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently

---

## Phase 5: User Story 3 - Execute MCP Tool Operations from AI Agent (Priority: P3)

**Goal**: Enable the AI agent to invoke appropriate MCP tools which perform database operations, with the results stored back in the conversation for continuity when the AI agent determines that a task operation is needed.

**Independent Test**: Can be fully tested by sending messages that trigger tool operations and verifying that both the tool calls are recorded and the database operations are performed correctly.

### Tests for User Story 3 (OPTIONAL - only if tests requested) ⚠️

- [ ] T027 [P] [US3] Integration test for MCP tool execution in backend/tests/integration/test_mcp_execution.py
- [ ] T028 [P] [US3] Contract test for MCP tool handling in backend/tests/contract/test_mcp_contract.py

### Implementation for User Story 3

- [ ] T029 [US3] Implement MCP tool integration in OpenAI Agent in backend/src/agents/todo_agent.py
- [ ] T030 [US3] Add ToolCall recording to ConversationService in backend/src/services/conversation_service.py
- [ ] T031 [US3] Update chat endpoint to handle tool call results in backend/src/api/v1/chat.py
- [ ] T032 [US3] Add MCP tool result storage to chat endpoint in backend/src/api/v1/chat.py
- [ ] T033 [US3] Integrate with User Story 1 and 2 components for full functionality

**Checkpoint**: All user stories should now be independently functional

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [ ] T034 [P] Documentation updates in backend/README.md
- [ ] T035 Code cleanup and refactoring across all components
- [ ] T036 Performance optimization across all stories
- [ ] T037 [P] Additional unit tests (if requested) in backend/tests/unit/
- [ ] T038 Security hardening for user isolation and data protection
- [ ] T039 Run quickstart.md validation to ensure setup instructions work

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
Task: "Implement OpenAI Agent with MCP tools integration in backend/src/agents/todo_agent.py"
Task: "Implement chat endpoint in backend/src/api/v1/chat.py"

# Launch all API components for User Story 1 together:
Task: "Add conversation history retrieval to chat endpoint in backend/src/api/v1/chat.py"
Task: "Add user message storage to chat endpoint in backend/src/api/v1/chat.py"
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