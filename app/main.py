from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import auth
from .database import Base, engine

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Authorization Service",
    description="A simple FastAPI authorization service with JWT authentication",
    version="1.0.0"
)

# CORS middleware - Allow frontend to connect
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",  # React dev server
        "http://127.0.0.1:3000",
        "http://localhost:8080",  # Vue/other dev servers
        "http://127.0.0.1:8080",
        "null",  # For file:// protocol (local HTML files)
        "http://localhost:5173",  # Vite dev server
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router)

@app.get("/")
async def root():
    return {"message": "Authorization Service API", "status": "running"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}