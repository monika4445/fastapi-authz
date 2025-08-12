from dotenv import load_dotenv
import os

load_dotenv()

try:
    from pydantic_settings import BaseSettings
except ImportError:
    from pydantic import BaseSettings

class Settings(BaseSettings):
    # Database
    database_url: str = os.getenv("DATABASE_URL", "postgresql+psycopg://postgres@localhost:5432/auth_db")
    
    # JWT
    secret_key: str = os.getenv("SECRET_KEY", "your-secret-key-here")
    algorithm: str = os.getenv("ALGORITHM", "HS256")
    access_token_expire_minutes: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))
    
    # Email settings (ADD THESE)
    email_user: str = os.getenv("EMAIL_USER", "")
    email_password: str = os.getenv("EMAIL_PASSWORD", "")
    frontend_url: str = os.getenv("FRONTEND_URL", "http://localhost:3000")
    
    class Config:
        env_file = ".env"
        extra = "ignore"

settings = Settings()
