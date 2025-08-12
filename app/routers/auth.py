# app/routers/auth.py
from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import User
from ..schemas import (
    UserCreate, UserResponse, Token, LoginRequest, 
    UserRegistrationResponse, EmailVerificationRequest, EmailVerificationResponse
)
from ..auth import (
    authenticate_user, create_access_token, get_password_hash, 
    generate_verification_token, verify_email_token
)
from ..dependencies import get_current_active_user
from ..config import settings
from ..email_service import email_service

router = APIRouter(prefix="/auth", tags=["authentication"])

@router.post("/register", response_model=UserRegistrationResponse, status_code=status.HTTP_201_CREATED)
async def register(user: UserCreate, db: Session = Depends(get_db)):
    # Check if user already exists
    db_user = db.query(User).filter(
        (User.email == user.email) | (User.username == user.username)
    ).first()
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email or username already registered"
        )
    
    # Generate verification token
    verification_token = generate_verification_token()
    
    # Create new user (unverified)
    hashed_password = get_password_hash(user.password)
    db_user = User(
        email=user.email,
        username=user.username,
        hashed_password=hashed_password,
        is_verified=False,
        verification_token=verification_token
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    # Send verification email
    email_sent = email_service.send_verification_email(
        to_email=user.email,
        username=user.username,
        verification_token=verification_token
    )
    
    if not email_sent:
        # If email fails, still return success but log the error
        print(f"⚠️ Failed to send verification email to {user.email}")
    
    return UserRegistrationResponse(
        message="Registration successful! Please check your email to verify your account.",
        user_id=db_user.id,
        email=db_user.email,
        username=db_user.username,
        verification_required=True
    )

@router.post("/verify-email", response_model=EmailVerificationResponse)
async def verify_email(verification: EmailVerificationRequest, db: Session = Depends(get_db)):
    # Verify the token and update user
    user = verify_email_token(db, verification.token)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid or expired verification token"
        )
    
    # Send welcome email
    email_service.send_welcome_email(
        to_email=user.email,
        username=user.username
    )
    
    return EmailVerificationResponse(
        message="Email verified successfully! You can now log in.",
        success=True,
        username=user.username
    )

@router.post("/login", response_model=Token)
async def login(login_data: LoginRequest, db: Session = Depends(get_db)):
    # First check if user exists
    user_check = db.query(User).filter(User.username == login_data.username).first()
    
    if not user_check:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Check if email is verified
    if not user_check.is_verified:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Email not verified. Please check your email and verify your account before logging in.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Authenticate user (this now also checks verification)
    user = authenticate_user(db, login_data.username, login_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/me", response_model=UserResponse)
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    return current_user

@router.post("/resend-verification")
async def resend_verification(email: str, db: Session = Depends(get_db)):
    """Resend verification email for unverified users"""
    user = db.query(User).filter(User.email == email).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User with this email not found"
        )
    
    if user.is_verified:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email is already verified"
        )
    
    # Generate new verification token
    verification_token = generate_verification_token()
    user.verification_token = verification_token
    db.commit()
    
    # Send verification email
    email_sent = email_service.send_verification_email(
        to_email=user.email,
        username=user.username,
        verification_token=verification_token
    )
    
    if not email_sent:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to send verification email"
        )
    
    return {"message": "Verification email sent successfully"}

@router.post("/logout")
async def logout():
    # In a real application, you might want to blacklist the token
    # For now, we'll just return a success message
    return {"message": "Successfully logged out"}