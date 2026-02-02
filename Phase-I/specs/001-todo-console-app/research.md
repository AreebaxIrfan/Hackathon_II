# Research: Phase I Todo In-Memory Console App

**Feature**: 001-todo-console-app
**Date**: 2026-01-02
**Status**: Complete

## Research Summary

### Phase 0: Technology and Architecture Decisions

#### Decision 1: In-Memory Storage Structure

**Options Considered**:
- Python `list` with indexing
- Python `dict` with ID as key
- Custom class with list backing store
- Database simulation layer

**Decision**: Python `list` with Todo objects

**Rationale**:
- Simple, efficient for single-user session (<1000 todos typical)
- Natural iteration order matches creation order (ID assignment)
- Built-in list methods provide all needed operations
- No overhead of dict lookups or custom implementations
- Direct mapping to spec requirement FR-003 (incrementing IDs)
- Satisfies success criteria SC-002 (<2s to view 50 todos)

**Trade-offs**:
- List lookups are O(n) for ID search - acceptable for <1000 items
- Dict would be O(1) but adds complexity for ordered iteration
- List preserves order naturally without extra logic

---

#### Decision 2: Todo Data Model

**Options Considered**:
- Dataclass (Python 3.7+)
- NamedTuple
- Custom class with properties
- Simple dict per todo

**Decision**: Python `dataclass`

**Rationale**:
- Clean, readable code (Principle IV)
- Automatic `__init__`, `__repr__`, `__eq__`
- Type hints improve code clarity
- Immutable by default (prevents accidental mutation)
- Built-in support for optional fields (description)
- No boilerplate required
- Industry standard for Python 3.7+ models

**Trade-offs**:
- NamedTuple would be lighter but immutable makes updates harder
- Custom class allows more control but requires boilerplate
- Dict is simplest but lacks type safety and structure

---

#### Decision 3: CLI Interaction Pattern

**Options Considered**:
- Command-line arguments (e.g., `app.py add "Buy groceries"`)
- Interactive menu loop
- Single-shot commands with flags
- REPL (Read-Eval-Print Loop)

**Decision**: Interactive menu loop

**Rationale**:
- Matches spec requirement FR-011 (graceful input handling)
- User-friendly for non-technical users (SC-006)
- Natural "session" feel for runtime-bound app
- Easier to guide users through options
- Reduces need for external documentation
- Aligns with typical CLI todo applications (e.g., various todo.txt implementations)

**Trade-offs**:
- Less scriptable than command-line arguments
- Requires more user interaction per operation
- Menu loop adds code complexity vs single-shot commands

---

#### Decision 4: Input Validation Strategy

**Options Considered**:
- Custom validator functions
- Third-party validation libraries
- Type coercion with try/except
- Regex patterns

**Decision**: Custom validator functions in CLI layer

**Rationale**:
- No external dependencies per constitution (Principle II)
- Clear, readable validation logic
- Reusable across CLI operations
- Specific error messages per FR-009
- Graceful handling per FR-011
- Simple to test and maintain

**Trade-offs**:
- More code than type coercion
- Less comprehensive than validation libraries
- Requires manual implementation of each validation rule

---

#### Decision 5: Error Handling Approach

**Options Considered**:
- Custom exception hierarchy
- Return codes with error messages
- Global exception handler
- Context managers for errors

**Decision**: Custom exceptions with CLI handling

**Rationale**:
- Clear separation of business errors vs system errors
- Enables service layer to signal specific error types
- CLI layer can translate to user-friendly messages
- Maintains separation of concerns (Principle IV)
- Traceable error paths from spec (FR-009)
- Supports graceful error handling (FR-011)

**Trade-offs**:
- More boilerplate than return codes
- Requires exception handling in CLI layer
- Potential for unhandled exceptions if not careful

---

## Architectural Decisions Summary

| Decision | Choice | Primary Benefit | Trade-off |
|-----------|---------|-----------------|------------|
| Storage | Python list | Simple, ordered iteration | O(n) lookup for ID |
| Data Model | dataclass | Type-safe, clean code | Immutable by default |
| CLI Pattern | Interactive menu | User-friendly, session feel | Less scriptable |
| Validation | Custom validators | Reusable, clear messages | More code to write |
| Error Handling | Custom exceptions | Clear error types, separation of concerns | More boilerplate |

## Technology Stack Confirmation

✅ **Python 3.13+**: Confirmed
✅ **UV**: Confirmed for dependency management
✅ **Standard library only**: No external dependencies per constitution
✅ **CLI interface**: Confirmed
✅ **In-memory storage**: Confirmed (list backing store)
✅ **No persistence**: Confirmed per Phase I scope

## Research Conclusion

All technical decisions align with:
- Constitution principles (I-VI)
- Phase I scope constraints
- Specification requirements (FR-001 through FR-012)
- Success criteria (SC-001 through SC-006)
- Non-functional requirements from spec

Architecture is simple, maintainable, and ready for task breakdown in Phase 2.
