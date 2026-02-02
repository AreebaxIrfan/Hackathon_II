---

description: "Task list for feature implementation"
---

# Tasks: Phase I Todo In-Memory Console App

**Input**: Design documents from `/specs/001-todo-console-app/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: NOT INCLUDED - Tests were not explicitly requested in feature specification. Implementation focuses on functional requirements only.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Single project**: `src/`, `tests/` at repository root
- Paths shown below follow single project structure from plan.md

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [x] T001 Create project structure per implementation plan
- [x] T002 Initialize Python 3.13+ project with UV
- [x] T003 Create pyproject.toml with standard library dependencies (none required)
- [x] T004 [P] Create directory structure: src/models, src/services, src/cli

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [x] T005 Create Todo data model in src/models/todo.py
- [x] T006 [P] Create custom NotFoundError exception in src/services/todo_service.py
- [x] T007 [P] Create TodoService class skeleton in src/services/todo_service.py
- [x] T008 Implement in-memory storage in TodoService: _todos list and _next_id counter
- [x] T009 Implement create_todo method in TodoService (FR-001, FR-002, FR-003)
- [x] T010 Implement get_all_todos method in TodoService (FR-004, FR-010)
- [x] T011 Implement get_todo_by_id method in TodoService (FR-009)
- [x] T012 Create input validator functions in src/cli/validator.py
- [x] T013 Implement validate_title function (checks empty/whitespace)
- [x] T014 Implement validate_id function (checks positive integer)
- [x] T015 Implement CLI display functions in src/cli/menu.py
- [x] T016 Implement display_todos function (formats todo list output)
- [x] T017 Implement display_menu function (shows 6 command options)
- [x] T018 [P] Implement display_message function (success/error messages)
- [x] T019 Create main.py skeleton with CLI entry point

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Create and View Todos (Priority: P1) 🎯 MVP

**Goal**: Enable users to add todos with title/description and view all todos with IDs, titles, and status

**Independent Test**: Create 2-3 todos with various title/description combinations, view list to verify all todos appear with correct IDs, titles, and status

### Implementation for User Story 1

- [x] T020 [P] [US1] Implement update_todo method in TodoService (FR-006, FR-007)
- [x] T021 [P] [US1] Implement delete_todo method in TodoService (FR-008)
- [x] T022 [P] [US1] Implement toggle_todo_status method in TodoService (FR-005)
- [x] T023 [US1] Implement handle_add_todo function in src/cli/menu.py (integrates create_todo, calls validator)
- [x] T024 [US1] Implement handle_view_todos function in src/cli/menu.py (integrates get_all_todos, calls display_todos)
- [x] T025 [US1] Wire up commands 1 and 2 in main.py CLI loop
- [x] T026 [US1] Add error handling for invalid titles in handle_add_todo
- [x] T027 [US1] Add "No todos" message handling in handle_view_todos

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently

---

## Phase 4: User Story 2 - Mark Todo Completion Status (Priority: P2)

**Goal**: Enable users to toggle todo status between complete/incomplete by referencing ID

**Independent Test**: Create 3 todos, mark 1 as complete, view list to confirm status changes, then mark it incomplete and verify status reverts

### Implementation for User Story 2

- [x] T028 [P] [US2] Implement handle_toggle_status function in src/cli/menu.py (integrates toggle_todo_status)
- [x] T029 [US2] Wire up command 5 in main.py CLI loop
- [x] T030 [US2] Add error handling for non-existent IDs in handle_toggle_status

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently

---

## Phase 5: User Story 3 - Update Todo Details (Priority: P3)

**Goal**: Enable users to update todo title and/or description by referencing ID

**Independent Test**: Create todo with title "Buy milk", update to "Buy 2% milk" with description "At store on Main St", view todo to confirm both fields changed

### Implementation for User Story 3

- [x] T031 [P] [US3] Implement handle_update_todo function in src/cli/menu.py (integrates update_todo)
- [x] T032 [US3] Wire up command 3 in main.py CLI loop
- [x] T033 [US3] Add partial update support (title-only, description-only, or both)
- [x] T034 [US3] Add error handling for empty title updates
- [x] T035 [US3] Add error handling for non-existent IDs in handle_update_todo

**Checkpoint**: User Stories 1, 2, AND 3 should now all work independently

---

## Phase 6: User Story 4 - Delete Todo (Priority: P4)

**Goal**: Enable users to remove todos from list by referencing ID

**Independent Test**: Create 5 todos, delete the 3rd one, view list to confirm 4 todos remain and deleted ID is no longer present

### Implementation for User Story 4

- [x] T036 [P] [US4] Implement handle_delete_todo function in src/cli/menu.py (integrates delete_todo)
- [x] T037 [US4] Wire up command 4 in main.py CLI loop
- [x] T038 [US4] Add error handling for non-existent IDs in handle_delete_todo

**Checkpoint**: All user stories should now be independently functional

---

## Phase 7: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [x] T039 [P] Create README.md with setup and run instructions
- [x] T040 [P] Verify main.py has no business logic (only CLI orchestration)
- [x] T041 [P] Verify error messages are clear and user-friendly (FR-004, FR-009)
- [x] T042 Implement CLI exit handling in main.py (command 6)
- [x] T043 Test all 5 user workflows end-to-end per SC-006
- [x] T044 Validate performance: add todo <5s per SC-001
- [x] T045 Validate performance: view 50 todos <2s per SC-002
- [x] T046 Validate performance: update/delete/toggle <3s per SC-003
- [x] T047 Test application stability: 30-minute session without crashes per SC-005
- [x] T048 Verify 100% of invalid operations show clear error messages per SC-004

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3-6)**: All depend on Foundational phase completion
  - User stories can then proceed in parallel (if staffed)
  - Or sequentially in priority order (P1 → P2 → P3 → P4)
- **Polish (Phase 7)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
  - Note: US1 implementation includes service methods that other stories need, but stories remain independently testable
- **User Story 2 (P2)**: Can start after Foundational (Phase 2) - Service method already implemented in US1 phase
  - CLI integration is independent - can test toggle status without add/update/delete
- **User Story 3 (P3)**: Can start after Foundational (Phase 2) - Service method already implemented in US1 phase
  - CLI integration is independent - can test updates without delete/toggle
- **User Story 4 (P4)**: Can start after Foundational (Phase 2) - Service method already implemented in US1 phase
  - CLI integration is independent - can test deletion without update/toggle

### Within Each User Story

- Models before services (completed in Foundational phase)
- Services before endpoints (service methods completed in Foundational/US1 phases)
- CLI handlers before main.py wiring
- All error handling added before story considered complete

### Parallel Opportunities

- All Setup tasks marked [P] can run in parallel
- All Foundational tasks marked [P] can run in parallel (within Phase 2)
- Once Foundational phase completes, all user stories can start in parallel (if team capacity allows)
- CLI handler functions within each story marked [P] can run in parallel
- Polish phase tasks marked [P] can run in parallel

---

## Parallel Example: User Story 1

```bash
# Launch all CLI handler implementations for User Story 1 together:
Task: "Implement handle_add_todo function in src/cli/menu.py (integrates create_todo, calls validator)"
Task: "Implement handle_view_todos function in src/cli/menu.py (integrates get_all_todos, calls display_todos)"

# These can run in parallel as they operate on different files and have no dependencies
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 3: User Story 1 (Create & View)
4. **STOP and VALIDATE**: Test User Story 1 independently
   - Add 2-3 todos with various title/description combos
   - View list to confirm all appear correctly
   - Test error handling (empty title, no todos)
5. Deploy/demo if ready (MVP delivers core value!)

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 → Test independently → Deploy/Demo (MVP!)
3. Add User Story 2 → Test independently → Deploy/Demo
4. Add User Story 3 → Test independently → Deploy/Demo
5. Add User Story 4 → Test independently → Deploy/Demo
6. Complete Polish phase → Final validation

Each story adds value without breaking previous stories

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together
2. Once Foundational is done:
   - Developer A: User Story 1 CLI integration (T023-T027)
   - Developer B: User Story 2 CLI integration (T028-T030)
   - Developer C: User Story 3 CLI integration (T031-T035)
   - Developer D: User Story 4 CLI integration (T036-T038)
3. Stories complete and integrate independently

Note: Service layer methods (T020-T022) are completed in US1 phase but benefit all stories

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Phase 2 (Foundational) blocks all user story work - complete this first
- Service methods for update/delete/toggle are implemented in US1 phase for efficiency
- Stories remain independently testable through CLI integration only
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence

---

## Task Summary

- **Total Tasks**: 48 tasks
- **Setup Phase**: 4 tasks
- **Foundational Phase**: 15 tasks (BLOCKS all user stories)
- **User Story 1 (P1)**: 8 tasks
- **User Story 2 (P2)**: 3 tasks
- **User Story 3 (P3)**: 5 tasks
- **User Story 4 (P4)**: 3 tasks
- **Polish Phase**: 10 tasks

**Parallel Opportunities**: 15 tasks marked with [P] can run in parallel
**MVP Scope**: 27 tasks (Setup + Foundational + US1) - delivers core value
