from sqlmodel import Session
from fastapi import HTTPException
from app.models import User
from app.schemas import UserCreate
from app.auth import hash_password, verify_password, create_access_token
from fastapi.security import OAuth2PasswordRequestForm

def register_admin_user(request: UserCreate, session: Session):
    existing_user = session.query(User).filter(
        (User.username == request.username) | (User.email == request.email)
    ).first()

    if existing_user:
        raise HTTPException(status_code=400, detail="Username or email already exists")

    new_admin = User(
        username=request.username,
        email=request.email,
        password_hash=hash_password(request.password),
        role="admin"
    )
    session.add(new_admin)
    session.commit()
    return {"message": "Admin registered successfully"}

def authenticate_admin(form_data: OAuth2PasswordRequestForm, session: Session):
    user = session.query(User).filter(User.username == form_data.username).first()
    if not user or user.role != "admin" or not verify_password(form_data.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid admin credentials")

    token = create_access_token({
        "sub": user.id,
        "username": user.username,
        "role": user.role
    })
    return {"access_token": token, "token_type": "bearer"}
