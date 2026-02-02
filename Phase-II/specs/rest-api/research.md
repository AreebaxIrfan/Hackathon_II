# Research for REST API Endpoints

## Technology Stack
- FastAPI: Modern, fast web framework for building APIs with Python 3.7+
- JWT: Industry standard for creating tokens that assert claims
- SQLModel: Combines SQLAlchemy and Pydantic for database modeling

## Best Practices for REST APIs
- Use standard HTTP methods (GET, POST, PUT, DELETE, PATCH)
- Use plural nouns for resource names (/tasks instead of /task)
- Use consistent naming conventions
- Return appropriate HTTP status codes
- Handle errors gracefully with descriptive messages

## JWT Authentication Patterns
- Use Authorization header with Bearer scheme
- Verify token signature server-side
- Extract user identity from token payload
- Validate token expiration

## API Security Considerations
- Input validation using Pydantic models
- Rate limiting (future consideration)
- SQL injection prevention (SQLModel handles this)
- User isolation through proper filtering

## Alternatives Considered
- OAuth 2.0: More complex than needed for this use case
- Session-based auth: Contradicts requirement to only verify JWT
- GraphQL: REST is sufficient for this use case