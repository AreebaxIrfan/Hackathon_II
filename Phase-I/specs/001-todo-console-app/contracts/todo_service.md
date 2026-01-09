# Contract: Todo Service

**Feature**: 001-todo-console-app
**Date**: 2026-01-02
**Status**: Complete

## Service Interface

### Purpose

Encapsulates all business logic for todo CRUD operations. Enforces validation rules, maintains in-memory state, and provides clean separation from CLI layer.

### Module

```python
src/services/todo_service.py
```

---

## Methods

### 1. `create_todo(title: str, description: str = "") -> Todo`

**Purpose**: Create a new todo item

**Inputs**:
- `title` (str, required): The todo title
- `description` (str, optional): Additional details, defaults to empty string

**Returns**: `Todo` object with assigned ID

**Preconditions**:
- Title must be non-empty string
- Title must not be whitespace-only

**Postconditions**:
- New todo added to in-memory list
- Todo ID is unique and increments from previous highest ID
- `is_complete` defaults to `False`
- Returns the created `Todo` object

**Errors**:
- `ValueError`: If title is empty or whitespace-only

**Spec Reference**: FR-001, FR-002, FR-003

---

### 2. `get_all_todos() -> List[Todo]`

**Purpose**: Retrieve all todos in the list

**Inputs**: None

**Returns**: List of all `Todo` objects (may be empty)

**Preconditions**: None

**Postconditions**:
- Returns complete list of todos
- Returns empty list if no todos exist
- Order preserved: first item has lowest ID

**Errors**: None

**Spec Reference**: FR-004, FR-010, FR-012

---

### 3. `get_todo_by_id(todo_id: int) -> Todo`

**Purpose**: Retrieve a specific todo by ID

**Inputs**:
- `todo_id` (int, required): The numeric identifier

**Returns**: `Todo` object with matching ID

**Preconditions**:
- `todo_id` must be a positive integer

**Postconditions**:
- Returns the `Todo` with matching ID
- Todos are returned in creation order

**Errors**:
- `NotFoundError`: If no todo with matching ID exists

**Spec Reference**: FR-009

---

### 4. `update_todo(todo_id: int, title: str = None, description: str = None) -> Todo`

**Purpose**: Update a todo's title and/or description

**Inputs**:
- `todo_id` (int, required): The numeric identifier
- `title` (str, optional): New title (if provided)
- `description` (str, optional): New description (if provided)

**Returns**: Updated `Todo` object

**Preconditions**:
- Todo with `todo_id` must exist
- If `title` provided, must be non-empty and not whitespace-only
- At least one of `title` or `description` must be provided

**Postconditions**:
- Todo title updated if `title` provided
- Todo description updated if `description` provided
- Unspecified fields remain unchanged
- ID and status cannot be changed via this method
- Returns updated `Todo` object

**Errors**:
- `NotFoundError`: If no todo with matching ID exists
- `ValueError`: If title is empty or whitespace-only

**Spec Reference**: FR-006, FR-007, FR-009

---

### 5. `delete_todo(todo_id: int) -> None`

**Purpose**: Remove a todo from the list

**Inputs**:
- `todo_id` (int, required): The numeric identifier

**Returns**: None

**Preconditions**:
- Todo with `todo_id` must exist

**Postconditions**:
- Todo removed from in-memory list
- Remaining todos retain original IDs (no reassignment)
- List size decreases by 1

**Errors**:
- `NotFoundError`: If no todo with matching ID exists

**Spec Reference**: FR-008, FR-009

---

### 6. `toggle_todo_status(todo_id: int) -> Todo`

**Purpose**: Toggle a todo's completion status

**Inputs**:
- `todo_id` (int, required): The numeric identifier

**Returns**: `Todo` object with updated status

**Preconditions**:
- Todo with `todo_id` must exist

**Postconditions**:
- `is_complete` flips: `True` → `False` or `False` → `True`
- All other fields remain unchanged
- Returns updated `Todo` object

**Errors**:
- `NotFoundError`: If no todo with matching ID exists

**Spec Reference**: FR-005, FR-009

---

## Exceptions

### `NotFoundError`

**Purpose**: Indicates a todo with specified ID does not exist

**Raised By**:
- `get_todo_by_id()`
- `update_todo()`
- `delete_todo()`
- `toggle_todo_status()`

**Message Format**: `"Todo with ID {todo_id} not found"`

**CLI Handling**: Display user-friendly error message per FR-009

---

### `ValueError`

**Purpose**: Indicates invalid input data

**Raised By**:
- `create_todo()` - empty/whitespace title
- `update_todo()` - empty/whitespace title

**Message Format**: `"Title cannot be empty"`

**CLI Handling**: Display user-friendly error message per FR-009

---

## State Management

### Internal State

```python
_todos: List[Todo] = []  # Private in-memory storage
_next_id: int = 1        # Counter for assigning IDs
```

### State Constraints

- `_todos` is never persisted (in-memory only per FR-012)
- `_next_id` starts at 1 and increments on each `create_todo()` call
- Deleted todos are removed from list, IDs never reused

---

## Performance Constraints

| Operation | Max Time | Notes |
|-----------|----------|-------|
| `create_todo()` | <100ms | Simple append, ID assignment |
| `get_all_todos()` | <2s | Per SC-002 for 50 todos |
| `get_todo_by_id()` | <50ms | Linear search O(n) |
| `update_todo()` | <50ms | Linear search + update |
| `delete_todo()` | <50ms | Linear search + removal |
| `toggle_todo_status()` | <50ms | Linear search + toggle |

**Note**: All operations satisfy SC-001/SC-002/SC-003 performance requirements.

---

## Thread Safety

**Scope**: Single-threaded, single-user session
**Concurrency**: Not supported per Phase I scope
**Locking**: Not required

---

## Testing Considerations

### Unit Tests (if added later)

- Test each method with valid inputs
- Test each method with invalid inputs
- Test state changes after operations
- Test edge cases (empty list, first item, last item)

### Integration Tests (if added later)

- Test service layer with CLI layer
- Test end-to-end workflows matching user stories
- Test error propagation from service to CLI

---

## Contract Completeness

✅ All functional requirements covered
✅ All error cases defined
✅ Performance constraints specified
✅ Pre/postconditions clear
✅ CLI handling guidance provided
✅ Traceability to spec maintained
