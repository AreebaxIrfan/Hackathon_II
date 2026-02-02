# Authentication & JWT Security

This project implements a secure user authentication system using Better Auth with JWT-based API access. Users can sign up, sign in, and access protected resources with proper authentication and authorization.

## Features

- User registration with email and password validation
- Secure JWT-based authentication
- Protected API endpoints with proper authorization
- Session-less architecture with stateless authentication
- Comprehensive error handling and logging
- Input validation and sanitization

## Tech Stack

- **Frontend**: Next.js 14 with App Router
- **Backend**: FastAPI with Python 3.9+
- **Database**: PostgreSQL (with SQLModel ORM)
- **Authentication**: JWT tokens with bcrypt password hashing
- **Security**: Environment-based secrets management

## Prerequisites

- Node.js 18+
- Python 3.9+
- PostgreSQL database

## Setup Instructions

### Backend Setup

1. Navigate to the backend directory:
```bash
cd backend
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
```bash
cp .env.example .env
```
Then update the .env file with your database connection details and a secure secret key.

5. Start the backend server:
```bash
uvicorn main:app --reload
```

The backend will be running at `http://localhost:8000`.

### Frontend Setup

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Set up environment variables:
```bash
cp .env.local.example .env.local
```
Then update the .env.local file with your backend API URL.

4. Start the development server:
```bash
npm run dev
```

The frontend will be running at `http://localhost:3000`.

## API Endpoints

### Authentication

- `POST /auth/register` - Register a new user
- `POST /auth/login` - Log in and get JWT token
- `GET /auth/me` - Get current user info

### Protected Endpoints

- `GET /api/profile` - Get user profile (requires authentication)
- `GET /api/dashboard` - Access dashboard (requires authentication)

## Security Features

- Passwords are hashed using bcrypt
- JWT tokens with limited expiration time (15 minutes)
- Proper input validation and sanitization
- Secure environment variable management
- Proper error handling without information disclosure

## Environment Variables

### Backend (.env)

- `DATABASE_URL` - PostgreSQL database connection string
- `SECRET_KEY` - Secret key for JWT signing (minimum 256 bits)
- `ALGORITHM` - JWT algorithm (default: HS256)
- `ACCESS_TOKEN_EXPIRE_MINUTES` - JWT expiration time (default: 15)

### Frontend (.env.local)

- `NEXT_PUBLIC_API_URL` - Backend API URL (e.g., http://localhost:8000)

## Development

### Running Tests

Backend tests:
```bash
pytest
```

### Code Style

- Backend: Follows PEP 8 guidelines
- Frontend: Uses ESLint and Prettier for consistent code style

## Deployment

1. Update environment variables for production
2. Set up a production-grade database
3. Configure proper CORS settings
4. Set up reverse proxy (nginx, Apache) with SSL termination
5. Use a process manager (PM2, systemd) for production deployment

## Troubleshooting

### Common Issues

- **JWT Expiration**: Tokens expire after 15 minutes; implement refresh logic in production
- **CORS Errors**: Ensure frontend domain is properly configured in backend CORS settings
- **Database Connection**: Verify database URL is correctly formatted

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License.