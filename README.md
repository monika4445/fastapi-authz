# FastAPI Authorization Service

A robust authorization service built with FastAPI, PostgreSQL, and JWT authentication.

## Features

- User registration and login
- JWT token-based authentication
- Password hashing with bcrypt
- PostgreSQL database integration
- Docker containerization
- Comprehensive API documentation
- Unit tests

## Quick Start

### Using Docker (Recommended)

1. Clone the repository:
```bash
git clone https://github.com/monika4445/fastapi-authz.git
cd fastapi-authz
```

2. Start the services:
```bash
docker-compose up --build
```

3. The API will be available at `http://localhost:8000`
4. API documentation at `http://localhost:8000/docs`

### Local Development

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Set up PostgreSQL and create a `.env` file based on `.env.example`

3. Run the application:
```bash
uvicorn app.main:app --reload
```

## API Endpoints

- `POST /auth/register` - Register a new user
- `POST /auth/login` - Login and get access token
- `GET /auth/me` - Get current user info (protected)
- `POST /auth/logout` - Logout user
- `GET /docs` - Swagger API documentation

## Testing

Run tests with:
```bash
pytest
```

## Environment Variables

Create a `.env` file with:
```env
DATABASE_URL=postgresql://user:password@localhost:5432/dbname
SECRET_KEY=your-secret-key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

## Commands to Run

### Development
```bash
# Clone your repo
git clone https://github.com/monika4445/fastapi-authz.git
cd fastapi-authz

# Install dependencies
pip install -r requirements.txt

# Run with Docker
docker-compose up --build

# Or run locally (need PostgreSQL running)
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Run tests
pytest

# Access API
# - API: http://localhost:8000
# - Docs: http://localhost:8000/docs
# - Health: http://localhost:8000/health
```

### Production
```bash
# Build and run with Docker
docker-compose up -d --build

# Or with specific environment
docker-compose -f docker-compose.prod.yml up -d
```

## Project Structure
```
fastapi-authz/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── config.py
│   ├── database.py
│   ├── models.py
│   ├── schemas.py
│   ├── auth.py
│   ├── dependencies.py
│   └── routers/
│       ├── __init__.py
│       └── auth.py
├── tests/
│   ├── __init__.py
│   ├── test_auth.py
│   └── conftest.py
├── .env.example
├── .gitignore
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── README.md
```

## Example Usage

### Register a new user
```bash
curl -X POST "http://localhost:8000/auth/register" \
     -H "Content-Type: application/json" \
     -d '{
       "email": "user@example.com",
       "username": "testuser",
       "password": "securepassword123"
     }'
```

### Login
```bash
curl -X POST "http://localhost:8000/auth/login" \
     -H "Content-Type: application/json" \
     -d '{
       "username": "testuser",
       "password": "securepassword123"
     }'
```

### Access protected route
```bash
curl -X GET "http://localhost:8000/auth/me" \
     -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

## Development Notes

- Python 3.12 required
- PostgreSQL database
- JWT tokens expire in 30 minutes by default
- Passwords are hashed using bcrypt
- CORS enabled for development (configure for production)

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License.