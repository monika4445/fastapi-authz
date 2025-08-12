# app/auth.py
from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from .config import settings
from .models import User
from .schemas import TokenData
import secrets
import string

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def generate_verification_token() -> str:
    """Generate a secure random verification token"""
    alphabet = string.ascii_letters + string.digits
    return ''.join(secrets.choice(alphabet) for _ in range(32))

def authenticate_user(db: Session, username: str, password: str) -> Optional[User]:
    user = db.query(User).filter(User.username == username).first()
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    # Check if user is verified
    if not user.is_verified:
        return None  # User exists but email not verified
    return user

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)
    return encoded_jwt

def verify_token(token: str) -> Optional[TokenData]:
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
        username: str = payload.get("sub")
        if username is None:
            return None
        token_data = TokenData(username=username)
        return token_data
    except JWTError:
        return None

def verify_email_token(db: Session, token: str) -> Optional[User]:
    """Verify email verification token and return user"""
    user = db.query(User).filter(User.verification_token == token).first()
    if not user:
        return None
    
    # Mark user as verified
    user.is_verified = True
    user.verification_token = None  # Clear the token
    user.verified_at = datetime.utcnow()
    db.commit()
    db.refresh(user)
    
    return user