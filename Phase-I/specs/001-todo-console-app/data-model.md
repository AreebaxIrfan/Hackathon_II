# Data Model: Phase I Todo In-Memory Console App

**Feature**: 001-todo-console-app
**Date**: 2026-01-02
**Status**: Complete

## Entity: Todo

### Overview

Represents a single task in the todo list with a unique identifier, required title, optional description, and completion status.

### Structure

```python
@dataclass
class Todo:
    """Represents a single todo item."""
    id: int                    # Unique numeric identifier (FR-003)
    title: str                 # Required title (FR-001, FR-002)
    description: str = ""      # Optional description (FR-001)
    is_complete: bool = False  # Completion status (FR-005)
```

### Field Descriptions

| Field | Type | Required | Description | Constraint |
|-------|------|----------|-------------|------------|
| `id` | `int` | Yes | Unique numeric identifier | Auto-assigned, incrementing, starting at 1 |
| `title` | `str` | Yes | The task title | Non-empty string (FR-002) |
| `description` | `str` | No | Additional details about the task | Defaults to empty string if not provided |
| `is_complete` | `bool` | No | Completion status | Defaults to `False` (incomplete) |

### Invariants

1. **ID Uniqueness**: Each todo has a unique ID within the session
2. **ID Assignment**: IDs start at 1 and increment by 1 for each new todo
3. **ID Persistence**: IDs are never reassigned after deletion (gaps remain)
4. **Title Validation**: Title cannot be empty or whitespace-only (FR-002, FR-007)
5. **Status Binary**: `is_complete` is either `True` or `False` (no intermediate states)

### Relationships

- **None**: Todo entities are independent with no relationships to other entities (Phase I scope)

## Storage Model

### In-Memory List

```python
todos: List[Todo] = []
```

### Storage Characteristics

- **Type**: Python `list` containing `Todo` objects
- **Lifetime**: Application runtime (resets on exit per FR-012)
- **Ordering**: Natural insertion order matches ID assignment order
- **Access**: Sequential iteration for display, linear search for ID lookup
- **Concurrency**: Single-threaded, single-user session

### Operations Supported

| Operation | Complexity | Description |
|-----------|------------|-------------|
| `append(todo)` | O(1) | Add new todo to end of list |
| `len(todos)` | O(1) | Get total count of todos |
| `for todo in todos` | O(n) | Iterate all todos for display |
| `find by id` | O(n) | Linear search for todo by ID |

## State Transitions

### Todo Status

```
┌─────────────┐
│  Incomplete │ ◄──┐
│ (False)     │    │ toggle
└──────┬──────┘    │
       │ toggle   │
       │          │
       ▼          │
┌─────────────┐    │
│  Complete   │ ───┘
│ (True)      │
└─────────────┘
```

### Lifecycle Events

1. **Creation**: Todo initialized with `id`, `title`, optional `description`, `is_complete=False`
2. **Update**: Fields modified (title, description) via ID reference
3. **Status Toggle**: `is_complete` flips `True` ↔ `False` via ID reference
4. **Deletion**: Todo removed from list via ID reference

## Validation Rules

### Create Operation (FR-001, FR-002)

- Title must be non-empty string
- Title must not be whitespace-only
- Description may be empty string
- ID is auto-assigned (not user-provided)
- `is_complete` defaults to `False`

### Update Operation (FR-006, FR-007)

- Target todo must exist (by ID)
- If updating title, must be non-empty
- If updating description, may be empty string
- ID cannot be changed
- Status cannot be changed via update (use toggle instead)

### Delete Operation (FR-008)

- Target todo must exist (by ID)
- Deletion removes todo from list
- Remaining todos keep original IDs (gaps remain)

### Toggle Status Operation (FR-005)

- Target todo must exist (by ID)
- Status flips: `True` → `False` or `False` → `True`
- All other fields unchanged

## Example Data

### Empty State

```python
todos = []  # No todos
```

### With Sample Todos

```python
todos = [
    Todo(id=1, title="Buy groceries", description="", is_complete=False),
    Todo(id=2, title="Write code", description="Finish feature implementation", is_complete=True),
    Todo(id=3, title="Review PR", description="", is_complete=False),
]
```

### After Deletion

```python
# After deleting todo ID 2
todos = [
    Todo(id=1, title="Buy groceries", description="", is_complete=False),
    Todo(id=3, title="Review PR", description="", is_complete=False),
]
# Note: ID 2 is gone, ID 3 remains unchanged
```

## Display Format

### List Display (FR-004)

```
Todos:
[1] Buy groceries                     (incomplete)
[2] Write code                        (complete)
[3] Review PR                         (incomplete)
```

### Empty List (FR-010)

```
No todos
```

## Data Model Completeness

✅ All functional requirements addressed (FR-001 through FR-012)
✅ Success criteria supported (SC-001 through SC-006)
✅ Constitution compliance verified
✅ Phase I scope respected
✅ In-memory constraint satisfied
