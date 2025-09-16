from sqlmodel import Session, select
from fastapi import HTTPException
from app.models import User
from app.schemas import UserCreate, UserLogin, UserRead
from app.auth import hash_password, verify_password, create_access_token

def register_user(user: UserCreate, session: Session) -> UserRead:
    existing_user = session.exec(select(User).where(User.email == user.email)).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_pw = hash_password(user.password)
    new_user = User(
        username=user.username,
        email=user.email,
        password_hash=hashed_pw,
        role="customer"
    )
    session.add(new_user)
    session.commit()
    session.refresh(new_user)

    return UserRead(**new_user.dict(exclude={"password_hash"}))

def authenticate_user(credentials: UserLogin, session: Session):
    user = session.exec(select(User).where(User.email == credentials.email)).first()
    if not user or not verify_password(credentials.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token({
        "sub": str(user.id),
        "username": user.username,
        "role": user.role
    })
    return {"access_token": token, "token_type": "bearer"}

def delete_user_by_id(user_id: int, session: Session):
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    session.delete(user)
    session.commit()
