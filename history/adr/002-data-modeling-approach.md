# ADR-002: Data Modeling Approach

## Status
Accepted

## Date
2026-01-28

## Context
We need to design a data model that supports:
- User-task relationships with proper ownership semantics
- Efficient querying of user-scoped data
- Data integrity and referential consistency
- Scalability for growing user and task volumes
- Support for common operations like filtering and sorting

The system must enforce that each task belongs to exactly one authenticated user, with proper foreign key relationships and indexing strategies.

## Decision
We will implement a normalized relational data model with:
- **User Entity**: UUID primary key, unique email, timestamps, activation status
- **Task Entity**: UUID primary key, foreign key to user, title/description/completion/priority fields, timestamps
- **Relationships**: Many-to-one (many tasks to one user) with cascading delete
- **Indexing Strategy**: Composite and single-column indexes for efficient user-scoped queries
- **Data Types**: UUID for IDs, proper field constraints and validation rules

This approach ensures data integrity while enabling efficient operations.

## Alternatives Considered
1. **Denormalized Approach**: Embedding user data in tasks would reduce joins but violate normalization principles and complicate updates
2. **Document-Based Model**: Storing tasks as nested documents under users would sacrifice SQL query capabilities
3. **Single Table with JSON**: Using a generic entity table with JSON fields would lose relational benefits and type safety
4. **Separate Tables Without Foreign Keys**: Would sacrifice data integrity for flexibility but increase risk of orphaned records
5. **Soft Deletes**: Keeping deleted records with flags instead of hard deletes would complicate queries and grow data volume

## Consequences
### Positive
- Strong data integrity through foreign key constraints
- Efficient user-scoped queries via targeted indexing
- Clear ownership semantics with cascading operations
- Support for complex queries and reporting
- Scalable design that handles growing datasets well
- Proper separation of concerns between entities

### Negative
- Additional complexity in query construction with joins
- Potential performance overhead for complex multi-table operations
- Need for careful index management to maintain performance
- Complexity in handling cascading deletes safely
- More complex data migration procedures if schema changes

## References
- specs/4-db-schema-persistence/plan.md
- specs/4-db-schema-persistence/research.md
- specs/4-db-schema-persistence/data-model.md