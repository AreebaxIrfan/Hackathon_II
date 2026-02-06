# Tasks: Frontend & Backend Validation

**Input**: Design documents from `/specs/001-validation-spec/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: The examples below include test tasks. Tests are OPTIONAL - only include them if explicitly requested in the feature specification.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Single project**: `src/`, `tests/` at repository root
- **Web app**: `backend/src/`, `frontend/src/`
- **Mobile**: `api/src/`, `ios/src/` or `android/src/`
- Paths shown below assume single project - adjust based on plan.md structure

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [X] T001 Create backend directory structure: `backend/src/models/`, `backend/src/services/`, `backend/src/api/`, `backend/src/mcp/`, `backend/src/agents/`
- [X] T002 Create frontend directory structure: `frontend/app/components/`, `frontend/app/lib/`, `frontend/app/chat/`, `frontend/public/`
- [X] T003 [P] Initialize backend project with FastAPI, SQLModel, Neon PostgreSQL dependencies
- [X] T004 [P] Initialize frontend project with Next.js 14, TypeScript, Tailwind CSS
- [X] T005 [P] Configure linting and formatting tools for both frontend and backend
- [X] T006 Create environment configuration files for both frontend and backend
- [X] T007 Set up Git repository structure with proper .gitignore files

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [X] T008 Set up database schema and migrations framework with SQLModel
- [X] T009 [P] Implement authentication/authorization framework with JWT
- [X] T010 [P] Setup API routing and middleware structure in FastAPI
- [X] T011 Create base models/entities that all stories depend on
- [X] T012 Configure error handling and logging infrastructure
- [X] T013 Setup database connection pool with Neon PostgreSQL
- [X] T014 [P] Implement security middleware for authentication validation
- [X] T015 Create database session management utilities

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Access Todo Application with Interactive Chatbot (Priority: P1) 🎯 MVP

**Goal**: Enable users to access the Todo application and interact with the chatbot to manage their tasks, with visible and correctly rendered UI components.

**Independent Test**: Can be fully tested by starting the frontend application, verifying all UI elements are visible and functional, and interacting with the chatbot to send/receive messages while performing basic Todo operations.

### Tests for User Story 1 (OPTIONAL - only if tests requested) ⚠️

- [ ] T016 [P] [US1] Contract test for POST /api/v1/chat/ endpoint in backend/tests/contract/test_chat.py
- [ ] T017 [P] [US1] Integration test for chat interaction flow in backend/tests/integration/test_chat_flow.py

### Implementation for User Story 1

- [X] T018 [P] [US1] Create Conversation model in backend/src/models/conversation.py
- [X] T019 [P] [US1] Create ChatMessage model in backend/src/models/chat_message.py
- [X] T020 [US1] Implement ChatService in backend/src/services/chat_service.py
- [X] T021 [US1] Implement POST /api/v1/chat/ endpoint in backend/src/api/chat_routes.py
- [X] T022 [US1] Create ChatComponent in frontend/app/components/ChatComponent.tsx
- [X] T023 [US1] Integrate chat interface into main Todo page in frontend/app/page.tsx
- [X] T024 [US1] Implement frontend chat API client in frontend/app/lib/chatClient.ts
- [X] T025 [US1] Add frontend chat state management in frontend/app/chat/store.ts
- [X] T026 [US1] Style and ensure chat UI renders correctly in frontend/app/components/ChatComponent.tsx
- [X] T027 [US1] Connect frontend chat to backend API endpoint
- [X] T028 [US1] Add loading states and error handling for chat interactions

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently

---

## Phase 4: User Story 2 - Verify Proper Application Structure and Code Organization (Priority: P1)

**Goal**: Ensure application code follows required structure with frontend code in frontend/app/ and backend code in backend/, relocating any legacy frontend code from frontend/src/ if needed.

**Independent Test**: Can be fully tested by examining the file structure and confirming that all frontend code is in designated directories and no backend code exists outside the backend directory.

### Tests for User Story 2 (OPTIONAL - only if tests requested) ⚠️

- [ ] T029 [P] [US2] File structure validation test in tests/integration/test_structure.py

### Implementation for User Story 2

- [X] T030 Audit frontend/src/ directory to identify all files that need relocation
- [X] T031 Move all files from frontend/src/ to frontend/app/ directory
- [X] T032 Verify no backend code exists outside backend/ directory
- [ ] T033 Update import paths in frontend code to reflect new app/ directory structure
- [ ] T034 Update Next.js configuration to use correct paths
- [X] T035 Remove empty frontend/src/ directory after successful migration
- [ ] T036 Verify build process works correctly with new structure
- [ ] T037 Update documentation to reflect new directory structure
- [ ] T038 Run linter and formatter on relocated files to ensure consistency

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently

---

## Phase 5: User Story 3 - Authenticate and Manage Tasks via Chat Interface (Priority: P2)

**Goal**: Allow authenticated users to use the chatbot to perform all basic Todo operations (create, read, update, delete tasks) through conversational commands while maintaining proper authentication.

**Independent Test**: Can be fully tested by authenticating as a user and using chat commands to perform all basic Todo operations successfully.

### Tests for User Story 3 (OPTIONAL - only if tests requested) ⚠️

- [ ] T039 [P] [US3] Contract test for Todo MCP tools in backend/tests/contract/test_mcp_tools.py
- [ ] T040 [P] [US3] Integration test for authenticated Todo operations via chat in backend/tests/integration/test_auth_todo_chat.py

### Implementation for User Story 3

- [X] T041 [P] [US3] Create Todo model in backend/src/models/todo.py
- [X] T042 [P] [US3] Create User model in backend/src/models/user.py
- [X] T043 [US3] Implement TodoService in backend/src/services/todo_service.py
- [ ] T044 [US3] Implement UserService in backend/src/services/user_service.py
- [X] T045 [US3] Create MCP server setup in backend/src/mcp/server.py
- [X] T046 [US3] Implement todo.create MCP tool in backend/src/mcp/todo_tools.py
- [X] T047 [US3] Implement todo.read MCP tool in backend/src/mcp/todo_tools.py
- [X] T048 [US3] Implement todo.update MCP tool in backend/src/mcp/todo_tools.py
- [X] T049 [US3] Implement todo.delete MCP tool in backend/src/mcp/todo_tools.py
- [X] T050 [US3] Implement OpenAI agent with MCP tool integration in backend/src/agents/todo_agent.py
- [ ] T051 [US3] Add authentication validation to MCP tools in backend/src/mcp/todo_tools.py
- [X] T052 [US3] Update chat endpoint to use authenticated user context
- [ ] T053 [US3] Add validation for user permissions in TodoService
- [ ] T054 [US3] Test Todo operations through chat interface with authentication

**Checkpoint**: At this point, all user stories should be independently functional

---

## Phase 6: Authentication & Authorization Enhancement

**Goal**: Strengthen authentication and authorization mechanisms to ensure proper access control for all operations.

- [X] T055 [P] Implement password hashing in User model
- [X] T056 [P] Add user registration endpoint in backend/src/api/auth_routes.py
- [X] T057 [P] Add login/logout endpoints in backend/src/api/auth_routes.py
- [ ] T058 Update JWT token handling in frontend with proper storage
- [ ] T059 Add user context to all Todo and Chat operations
- [ ] T060 Add permission checks to ensure data isolation
- [ ] T061 Implement refresh token mechanism if needed

---

## Phase 7: Frontend & Backend Integration

**Goal**: Ensure seamless integration between frontend and backend components with proper error handling.

- [X] T062 [P] Implement GET /api/v1/todos/ endpoint in backend/src/api/todo_routes.py
- [X] T063 [P] Implement POST /api/v1/todos/ endpoint in backend/src/api/todo_routes.py
- [X] T064 Implement PUT /api/v1/todos/{id} endpoint in backend/src/api/todo_routes.py
- [X] T065 Implement DELETE /api/v1/todos/{id} endpoint in backend/src/api/todo_routes.py
- [X] T066 Create Todo management UI components in frontend/app/components/TodoList.tsx
- [X] T067 Connect frontend Todo operations to backend API in frontend/app/lib/todoClient.ts
- [ ] T068 Add real-time synchronization between chat and Todo list
- [ ] T069 Handle API errors gracefully in frontend components
- [ ] T070 Implement offline capability for basic operations if needed

---

## Phase 8: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [ ] T071 [P] Documentation updates in docs/
- [ ] T072 Code cleanup and refactoring across all components
- [ ] T073 Performance optimization for chat and Todo operations
- [ ] T074 [P] Additional unit tests in backend/tests/unit/ and frontend/tests/
- [ ] T075 Security hardening of all endpoints and user inputs
- [ ] T076 Run quickstart.md validation to ensure setup process works
- [ ] T077 Update README with current project structure and setup instructions
- [ ] T078 Add environment variable validation in both frontend and backend
- [ ] T079 Implement comprehensive logging for debugging and monitoring

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
- **User Story 2 (P1)**: Can start after Foundational (Phase 2) - May integrate with US1 but should be independently testable
- **User Story 3 (P2)**: Can start after Foundational (Phase 2) - May integrate with US1/US2 but should be independently testable

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
Task: "Contract test for POST /api/v1/chat/ endpoint in backend/tests/contract/test_chat.py"
Task: "Integration test for chat interaction flow in backend/tests/integration/test_chat_flow.py"

# Launch all models for User Story 1 together:
Task: "Create Conversation model in backend/src/models/conversation.py"
Task: "Create ChatMessage model in backend/src/models/chat_message.py"
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