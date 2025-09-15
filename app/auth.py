from passlib.context import CryptContext
from jose import jwt, JWTError, ExpiredSignatureError
from datetime import datetime, timedelta
from typing import Optional
from fastapi import Depends, HTTPException, status
from app.models import User

# Secret key for JWT (use .env in production)
SECRET_KEY = "arian"  # make sure this matches everywhere
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = {
        "sub": str(data.get("sub")),       # ✅ Ensure sub is a string
        "username": data.get("username"),
        "role": data.get("role"),
        "exp": datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    }
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
