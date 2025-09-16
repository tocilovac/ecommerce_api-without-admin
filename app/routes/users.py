from fastapi import APIRouter, Depends, status
from sqlmodel import Session
from app.database import get_session
from app.schemas import UserCreate, UserLogin, UserRead
from app.dependencies import require_admin
from app.services.users_service import(
    register_user,
    authenticate_user,
    delete_user_by_id
)

router = APIRouter(prefix="/users", tags=["users"])

@router.post("/register", response_model=UserRead)
def register(user: UserCreate, session: Session = Depends(get_session)):
    return register_user(user, session)

@router.post("/login")
def login(credentials: UserLogin, session: Session = Depends(get_session)):
    return authenticate_user(credentials, session)

@router.delete("/{user_id}", status_code=204, dependencies=[Depends(require_admin)])
def delete_user(user_id: int, session: Session = Depends(get_session)):
    return delete_user_by_id(user_id, session)