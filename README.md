# 🔐 FastAPI Authentication Service

A modern, full-stack authentication service with email verification built using FastAPI, PostgreSQL, and JWT tokens. Features a beautiful responsive frontend and production-ready backend.

## ✨ Features

- **Secure Authentication** - JWT token-based authentication with bcrypt password hashing
- **Email Verification** - Required email verification before account activation
- **Modern Frontend** - Beautiful, responsive web interface with real-time feedback
- **Security Best Practices** - Protected routes, token expiration, and secure password storage
- **PostgreSQL Integration** - Robust database with SQLAlchemy ORM
- **Docker Ready** - Complete containerization for easy deployment
- **Auto-Generated Docs** - Interactive API documentation with Swagger UI
- **Comprehensive Testing** - Full test suite with pytest
- **Production Ready** - Error handling, logging, and fallback mechanisms

## 🚀 Quick Start

### Prerequisites

- **Python 3.12+**
- **PostgreSQL 14+**
- **Git**

### 1. Clone Repository

```bash
git clone https://github.com/monika4445/fastapi-authz.git
cd fastapi-authz
```

### 2. Environment Setup

Create a `.env` file in the project root:

```env
# Database Configuration
DATABASE_URL=postgresql+psycopg://postgres@localhost:5432/auth_db

# JWT Configuration
SECRET_KEY=your-super-secret-jwt-key-change-this-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Email Configuration (Gmail)
EMAIL_USER=your-email@gmail.com
EMAIL_PASSWORD=your-gmail-app-password
FRONTEND_URL=http://localhost:3000
```

### 3. Database Setup

```bash
# Create PostgreSQL database
psql -U postgres -c "CREATE DATABASE auth_db;"

# Or using Docker
docker run --name postgres-auth -e POSTGRES_PASSWORD=password -e POSTGRES_DB=auth_db -p 5432:5432 -d postgres:15
```

### 4. Install Dependencies

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install packages
pip install -r requirements.txt
```

### 5. Run the Application

**Terminal 1 - Backend (Port 8000):**
```bash
uvicorn app.main:app --reload
```

**Terminal 2 - Frontend (Port 3000):**
```bash
cd frontend
python start_frontend.py
```

### 6. Access the Application

- **Frontend UI:** http://localhost:3000
- **Backend API:** http://localhost:8000
- **API Documentation:** http://localhost:8000/docs
- **Health Check:** http://localhost:8000/health

## 🐳 Docker Deployment (Alternative)

### Quick Docker Start

```bash
# Start both database and application
docker-compose up --build

# Run in background
docker-compose up -d --build
```

### Individual Services

```bash
# Database only
docker-compose up -d db

# Application only (requires database)
docker-compose up web
```

## 📱 How to Use

### 1. User Registration

1. Open http://localhost:3000
2. Click **"Register"** tab
3. Fill in:
   - Email address
   - Username
   - Password
4. Click **"Register"**
5. Check console output for verification link (demo mode) or your email inbox

### 2. Email Verification

**Demo Mode (Console):**
- Copy verification link from terminal output
- Paste in browser address bar
- Account verified instantly

**Production Mode (Real Email):**
- Check your email inbox
- Click verification button in email
- Redirected to application with verified account

### 3. Login & Access

1. Click **"Login"** tab
2. Enter username and password
3. Click **"Login"**
4. Access granted - redirected to profile
5. View your secure profile information

### 4. Profile Management

- View account details
- Check verification status
- See registration date
- Logout securely

## 🔗 API Endpoints

### Authentication Routes

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| `POST` | `/auth/register` | Register new user | ❌ |
| `POST` | `/auth/verify-email` | Verify email address | ❌ |
| `POST` | `/auth/login` | Login user | ❌ |
| `GET` | `/auth/me` | Get user profile | ✅ |
| `POST` | `/auth/resend-verification` | Resend verification email | ❌ |
| `POST` | `/auth/logout` | Logout user | ✅ |

### System Routes

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/` | Root endpoint |
| `GET` | `/health` | Health check |
| `GET` | `/docs` | API documentation |

### Example API Usage

**Register User:**
```bash
curl -X POST "http://localhost:8000/auth/register" \
     -H "Content-Type: application/json" \
     -d '{
       "email": "user@example.com",
       "username": "newuser",
       "password": "securepass123"
     }'
```

**Login:**
```bash
curl -X POST "http://localhost:8000/auth/login" \
     -H "Content-Type: application/json" \
     -d '{
       "username": "newuser",
       "password": "securepass123"
     }'
```

**Access Protected Route:**
```bash
curl -X GET "http://localhost:8000/auth/me" \
     -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

## 📧 Email Configuration

### Gmail Setup (Recommended)

1. **Enable 2-Factor Authentication** on your Gmail account
2. **Generate App Password:**
   - Visit: https://myaccount.google.com/apppasswords
   - App: Mail
   - Device: Other (FastAPI Auth)
   - Copy 16-character password
3. **Update .env file:**
   ```env
   EMAIL_USER=your-email@gmail.com
   EMAIL_PASSWORD=abcd efgh ijkl mnop  # Keep spaces as shown
   ```

## 🧪 Testing

### Run Test Suite

```bash
# All tests
pytest

# With coverage
pytest --cov=app

# Specific test file
pytest tests/test_auth.py

# Verbose output
pytest -v
```

### Manual Testing

```bash
# Test database connection
python -c "from app.database import engine; print('✅ Database connected!')"

# Test Gmail credentials (if configured)
python test_gmail_fixed.py

# Test API health
curl http://localhost:8000/health
```

## 🔧 Configuration

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `DATABASE_URL` | `postgresql+psycopg://postgres@localhost:5432/auth_db` | PostgreSQL connection string |
| `SECRET_KEY` | `your-secret-key` | JWT signing secret |
| `ALGORITHM` | `HS256` | JWT algorithm |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | `30` | Token expiration time |
| `EMAIL_USER` | `""` | Gmail username |
| `EMAIL_PASSWORD` | `""` | Gmail app password |
| `FRONTEND_URL` | `http://localhost:3000` | Frontend URL for email links |

### Database Migration

```bash
# Create new migration
alembic revision --autogenerate -m "description"

# Apply migrations
alembic upgrade head

# Manual database setup
python migrate_db.py
```

## 🐛 Troubleshooting

### Common Issues

**Database Connection Failed:**
```bash
# Check PostgreSQL status
pg_ctl status

# Restart PostgreSQL
brew services restart postgresql  # macOS
sudo systemctl restart postgresql  # Linux
```

**Email Not Sending:**
- Check Gmail 2FA is enabled
- Verify app password format (19 characters with spaces)
- Application falls back to console mode automatically

**Frontend Not Loading:**
```bash
# Check if port 3000 is available
lsof -i :3000

# Start frontend server manually
cd frontend && python start_frontend.py
```

**JWT Token Errors:**
- Check SECRET_KEY is set in .env
- Verify token hasn't expired (30 min default)
- Ensure Bearer prefix in Authorization header

## 🚀 Production Deployment

### Environment Setup

```env
# Production .env
DATABASE_URL=postgresql://user:pass@production-db:5432/auth_db
SECRET_KEY=super-long-random-production-secret-key
EMAIL_USER=noreply@yourdomain.com
EMAIL_PASSWORD=production-app-password
FRONTEND_URL=https://yourdomain.com
```

### Docker Production

```bash
# Build production image
docker build -t fastapi-auth .

# Run with production config
docker-compose -f docker-compose.prod.yml up -d
```

### Security Checklist

- [ ] Change default SECRET_KEY
- [ ] Use environment-specific database
- [ ] Enable HTTPS
- [ ] Configure CORS for production domains
- [ ] Set up email monitoring
- [ ] Enable database backups
- [ ] Configure log rotation

## 🤝 Contributing

1. Fork the repository
2. Create feature branch: `git checkout -b feature/amazing-feature`
3. Commit changes: `git commit -m 'Add amazing feature'`
4. Push to branch: `git push origin feature/amazing-feature`
5. Open Pull Request

## 📄 License

This project is licensed under the MIT License.
---

**Built with ❤️ using FastAPI, PostgreSQL, and modern web technologies**