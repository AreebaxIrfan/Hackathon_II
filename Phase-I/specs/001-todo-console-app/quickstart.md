# Quickstart: Phase I Todo In-Memory Console App

**Feature**: 001-todo-console-app
**Date**: 2026-01-02
**Status**: Complete

## Prerequisites

- Python 3.13 or later installed
- UV package manager installed
- Git (for repository management)
- Command-line terminal (Windows PowerShell, Linux bash, or macOS Terminal)

---

## Installation

### 1. Clone or Initialize Repository

```bash
# If starting from template
git clone <repository-url>
cd Phase1

# OR if working locally
cd /path/to/Phase1
```

### 2. Set Up Python Environment with UV

```bash
# Create virtual environment and install dependencies
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# For this project, no external dependencies required
# Standard library only per constitution
```

### 3. Verify Setup

```bash
# Check Python version (must be 3.13+)
python --version

# Verify UV is installed
uv --version

# Verify Git is initialized (if applicable)
git status
```

---

## Running the Application

### Start the Todo App

```bash
# From project root
python src/main.py
```

### Expected Output

```
=======================================
  Todo Console App
=======================================

Commands:
  1. Add Todo
  2. View Todos
  3. Update Todo
  4. Delete Todo
  5. Mark Complete/Incomplete
  6. Exit

Enter command (1-6): _
```

---

## Basic Usage Examples

### 1. Add a Todo

**Command**: `1` (Add Todo)

**Example**:
```
Enter command (1-6): 1
Enter title: Buy groceries
Enter description (press Enter to skip): Get milk and eggs

✓ Todo added: [1] Buy groceries (incomplete)
```

**Without description**:
```
Enter command (1-6): 1
Enter title: Call dentist
Enter description (press Enter to skip):

✓ Todo added: [2] Call dentist (incomplete)
```

---

### 2. View All Todos

**Command**: `2` (View Todos)

**Example with todos**:
```
Enter command (1-6): 2

Todos:
[1] Buy groceries - Get milk and eggs  (incomplete)
[2] Call dentist                         (incomplete)
[3] Write code                           (complete)
```

**Example with no todos**:
```
Enter command (1-6): 2

No todos
```

---

### 3. Update a Todo

**Command**: `3` (Update Todo)

**Update title only**:
```
Enter command (1-6): 3
Enter todo ID: 2
Enter new title (press Enter to keep current): Schedule dental appointment
Enter new description (press Enter to keep current):

✓ Todo updated: [2] Schedule dental appointment (incomplete)
```

**Update description only**:
```
Enter command (1-6): 3
Enter todo ID: 1
Enter new title (press Enter to keep current):
Enter new description (press Enter to keep current): Get milk, eggs, and bread

✓ Todo updated: [1] Buy groceries - Get milk, eggs, and bread (incomplete)
```

**Update both**:
```
Enter command (1-6): 3
Enter todo ID: 3
Enter new title (press Enter to keep current): Fix bug in authentication
Enter new description (press Enter to keep current): User token expires after 1 hour

✓ Todo updated: [3] Fix bug in authentication (complete)
```

---

### 4. Delete a Todo

**Command**: `4` (Delete Todo)

**Example**:
```
Enter command (1-6): 4
Enter todo ID: 2

✓ Todo deleted: [2] Schedule dental appointment
```

**Error case**:
```
Enter command (1-6): 4
Enter todo ID: 99

✗ Error: Todo with ID 99 not found
```

---

### 5. Mark Complete/Incomplete

**Command**: `5` (Mark Complete/Incomplete)

**Mark as complete**:
```
Enter command (1-6): 5
Enter todo ID: 1

✓ Todo marked as complete: [1] Buy groceries
```

**Mark as incomplete**:
```
Enter command (1-6): 5
Enter todo ID: 3

✓ Todo marked as incomplete: [3] Write code
```

**Error case**:
```
Enter command (1-6): 5
Enter todo ID: 10

✗ Error: Todo with ID 10 not found
```

---

### 6. Exit Application

**Command**: `6` (Exit)

**Example**:
```
Enter command (1-6): 6

Goodbye!
```

---

## Common Error Messages

| Error | Cause | Resolution |
|-------|-------|------------|
| `Todo with ID X not found` | Referenced non-existent todo ID | Check your ID with "View Todos" |
| `Title cannot be empty` | Provided empty or whitespace-only title | Enter a non-empty title |
| `Invalid command` | Entered command outside 1-6 range | Enter a number between 1 and 6 |
| `Invalid ID` | Provided non-numeric ID | Enter a numeric ID |

---

## Tips

- **View frequently**: Use "View Todos" after add/update/delete operations to confirm changes
- **IDs are permanent**: Deleting a todo does not reassign IDs (gaps remain)
- **Session-bound**: All todos are lost when you exit the application (in-memory only)
- **Descriptions are optional**: Press Enter to skip description field
- **Partial updates**: When updating, press Enter to keep current value

---

## Validation Checklist

After implementation, validate all 5 features work:

- [ ] **Add Todo**: Create 3+ todos with and without descriptions
- [ ] **View Todos**: Display list shows IDs, titles, status correctly
- [ ] **Update Todo**: Update title, description, or both successfully
- [ ] **Delete Todo**: Remove todo and confirm ID not reused
- [ ] **Toggle Status**: Mark todos complete/incomplete correctly
- [ ] **Error Handling**: Invalid IDs, empty titles, invalid commands show clear messages

---

## Troubleshooting

### "Python not found" error

Ensure Python 3.13+ is installed and added to PATH:

```bash
# Check Python version
python --version

# If not found, install from https://www.python.org/downloads/
```

### "Module not found" error

Ensure you're in the project root and dependencies are installed:

```bash
# Verify current directory
pwd  # Linux/macOS
cd   # Windows

# For this project, no external dependencies required
# Only standard library used
```

### Application crashes unexpectedly

Check for:
1. Python version (must be 3.13+)
2. Proper directory structure (src/ folder exists)
3. All source files present (main.py, todo.py, todo_service.py, menu.py)

---

## Next Steps

1. Complete all validation checklist items
2. Run `/sp.tasks` to generate implementation tasks
3. Run `/sp.implement` to build the application
4. Test all 5 user stories from the specification
5. Verify success criteria SC-001 through SC-006

---

## Support

For issues or questions:
- Check the specification: `specs/001-todo-console-app/spec.md`
- Review the constitution: `.specify/memory/constitution.md`
- Consult the CLAUDE.md: `CLAUDE.md`
