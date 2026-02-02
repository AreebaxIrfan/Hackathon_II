# ADR-001: Database Technology Stack

## Status
Accepted

## Date
2026-01-28

## Context
We need to select a robust, scalable database solution for the task management application that supports:
- Reliable persistence of user and task data
- Strong data integrity constraints
- Type safety across database and API layers
- Efficient querying for user-scoped operations
- Integration with the existing Python/FastAPI backend

The requirements mandate using SQLModel for database models and Neon PostgreSQL for the database backend.

## Decision
We will use the following integrated database technology stack:
- **ORM Layer**: SQLModel (combining SQLAlchemy and Pydantic)
- **Database**: Neon PostgreSQL (PostgreSQL-compatible cloud database)
- **Migration Tool**: Alembic (integrated with SQLModel)
- **Connection Management**: Environment variables with connection pooling

This decision integrates multiple related technologies that work together as a cohesive solution.

## Alternatives Considered
1. **Raw SQLAlchemy + Separate Pydantic Models**: More verbose approach requiring separate validation models, increasing code duplication and maintenance overhead
2. **Django ORM**: Heavy framework overhead that would require significant architectural changes and impose Django's patterns
3. **NoSQL Solution (MongoDB/Redis)**: Would contradict the requirement to use a relational database with foreign key relationships
4. **SQLite**: Insufficient for production requirements and doesn't meet the Neon PostgreSQL mandate
5. **Peewee ORM**: Less mature ecosystem compared to SQLAlchemy, limited Pydantic integration

## Consequences
### Positive
- Unified data modeling across database and API layers through SQLModel
- Strong type safety with Pydantic validation baked into models
- Robust data integrity through PostgreSQL foreign key constraints
- Automatic migration support via Alembic integration
- Cloud-native scalability with Neon's PostgreSQL service
- Familiar SQL-based querying with SQLAlchemy's power

### Negative
- Learning curve for SQLModel if team is unfamiliar with SQLAlchemy
- PostgreSQL-specific features may create vendor lock-in
- Additional complexity compared to simpler solutions like SQLite
- Potential costs associated with Neon PostgreSQL service

## References
- specs/4-db-schema-persistence/plan.md
- specs/4-db-schema-persistence/research.md
- specs/4-db-schema-persistence/data-model.md