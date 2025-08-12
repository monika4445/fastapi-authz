# app/schemas.py
from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

class UserBase(BaseModel):
    email: EmailStr
    username: str

class UserCreate(UserBase):
    password: str

class UserResponse(UserBase):
    id: int
    is_active: bool
    is_verified: bool
    created_at: datetime
    verified_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

class UserRegistrationResponse(BaseModel):
    message: str
    user_id: int
    email: str
    username: str
    verification_required: bool = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

class LoginRequest(BaseModel):
    username: str
    password: str

class EmailVerificationRequest(BaseModel):
    token: str

class EmailVerificationResponse(BaseModel):
    message: str
    success: bool
    username: str