# Data Model for Authentication & JWT Security

## JWT Token Structure

### JWT Header
- `alg`: Algorithm used for signing (HS256)
- `typ`: Token type (JWT)

### JWT Payload Claims
- `sub`: Subject (user ID) - required
- `email`: User email address - required
- `iat`: Issued at timestamp - required
- `exp`: Expiration timestamp - required
- `jti`: JWT ID for token tracking (optional)

### JWT Signature
- Computed using HMAC SHA-256 with shared secret
- Verifies token authenticity and integrity

## Token Storage Model

### Browser Storage Options
- httpOnly Cookie: Automatic inclusion in requests, XSS protection
- localStorage: Programmatic access for API calls, vulnerable to XSS
- sessionStorage: Temporary storage, cleared on tab close

### Recommended Storage Strategy
- Primary: httpOnly cookies with SameSite and Secure attributes
- Fallback: Secure localStorage with additional validation

## User Identity Model

### Claims Extracted from JWT
- `user_id`: Unique identifier for the authenticated user
- `email`: User's email address for identification
- `roles`: User roles/permissions (not used in this implementation)
- `exp`: Token expiration timestamp for validation

### Identity Verification Process
1. Extract token from Authorization header
2. Verify signature using shared secret
3. Validate expiration timestamp
4. Extract user identity claims
5. Attach identity to request context

## Session State Model

### Stateless Authentication
- No server-side session storage
- Authentication state contained in JWT
- Each request independently verified
- No session cleanup required

### Authentication Status
- Authenticated: Valid JWT present and verified
- Unauthenticated: No JWT or invalid JWT
- Expired: JWT present but past expiration time

## Security Attributes

### Token Security Features
- Expiration time limits window of compromise
- Signed with secure algorithm to prevent tampering
- Compact format suitable for HTTP headers
- Self-contained with all necessary claims

### Storage Security Measures
- HttpOnly flag prevents JavaScript access
- Secure flag ensures HTTPS transmission
- SameSite attribute prevents CSRF attacks
- Domain/path restrictions limit scope

## Token Lifecycle

### Creation Flow
1. User authenticates successfully
2. Server generates JWT with user claims
3. Token signed with shared secret
4. Token returned to client for storage

### Verification Flow
1. Client includes token in Authorization header
2. Server extracts and parses token
3. Signature verified against shared secret
4. Claims validated (expiration, etc.)
5. User identity extracted for request

### Expiration Flow
1. Token reaches expiration time
2. Server rejects requests with expired token
3. Client receives 401 Unauthorized response
4. Client redirects to login or refreshes token