# Quickstart Guide for Authentication & JWT Security

## Setup Overview

This guide walks through setting up the secure authentication system using Better Auth with JWT-based API access.

## Prerequisites

- Node.js 18+ for frontend
- Python 3.9+ for backend
- Understanding of JWT concepts
- Environment for secret management

## Frontend Setup

### 1. Install Better Auth
```bash
npm install better-auth
```

### 2. Configure Better Auth with JWT
```javascript
// lib/auth.js or similar
import { initAuth } from 'better-auth';

const auth = initAuth({
  // Configuration options for JWT-based auth
});
```

### 3. Implement Login/Registration Components
- Create login form with email/password fields
- Implement registration form
- Handle authentication state in React context
- Store JWT tokens securely in httpOnly cookies or localStorage

## Backend Setup

### 1. Install JWT Dependencies
```bash
pip install python-jose[cryptography] passlib[bcrypt]
```

### 2. Configure JWT Settings
```python
# core/config.py
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 15
```

### 3. Create JWT Utility Functions
```python
# auth/jwt.py
from jose import JWTError, jwt
from datetime import datetime, timedelta

def create_access_token(data: dict, expires_delta: timedelta = None):
    # Implementation for creating JWT
    pass

def verify_token(token: str):
    # Implementation for verifying JWT
    pass
```

## JWT Middleware Implementation

### 1. Create Authentication Dependency
```python
# dependencies/auth.py
from fastapi import HTTPException, status
from auth.jwt import verify_token

async def get_current_user(token: str = Security(oauth2_scheme)):
    # Verify token and return current user
    pass
```

### 2. Apply to Protected Routes
```python
# api/protected_routes.py
@app.get("/protected")
async def protected_route(current_user: User = Depends(get_current_user)):
    # Access user information from JWT
    pass
```

## Security Configuration

### 1. Environment Variables
```bash
# .env
SECRET_KEY=your-super-long-and-secure-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=15
```

### 2. CORS Configuration
```python
# main.py
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://your-frontend-domain.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    # Allow authorization header
    allow_headers=["Authorization"],
)
```

## Testing Authentication Flow

### 1. Registration Flow
```bash
curl -X POST http://localhost:8000/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email": "test@example.com", "password": "password123"}'
```

### 2. Login Flow
```bash
curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email": "test@example.com", "password": "password123"}'
```

### 3. Protected Route Access
```bash
curl -X GET http://localhost:8000/protected/route \
  -H "Authorization: Bearer YOUR_JWT_TOKEN_HERE"
```

### 4. Unauthorized Access Test
```bash
curl -X GET http://localhost:8000/protected/route
# Should return 401 Unauthorized
```

## Common Issues and Troubleshooting

### Token Expiration
- JWT tokens have a limited lifetime (15 minutes by default)
- Implement token refresh mechanisms for better UX
- Handle 401 responses gracefully in frontend

### CORS Problems
- Ensure frontend domain is properly configured in backend CORS settings
- Verify that Authorization header is allowed in CORS configuration

### Secret Key Security
- Never commit secret keys to version control
- Use environment variables for secret management
- Rotate keys periodically in production

## Security Best Practices

1. Use strong secret keys (>256 bits)
2. Implement short token expiration times
3. Store tokens securely (httpOnly cookies preferred)
4. Validate token claims on every request
5. Use HTTPS in production environments
6. Sanitize and validate all inputs
7. Monitor authentication attempts for suspicious activity