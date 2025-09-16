from fastapi import APIRouter, Depends
from sqlmodel import Session
from app.database import get_session
from app.schemas import UserCreate, TokenResponse
from app.services.admin_service import register_admin_user, authenticate_admin
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter(prefix="/admin", tags=["Admin"])

@router.post("/register")
def register_admin(request: UserCreate, session: Session = Depends(get_session)):
    return register_admin_user(request, session)

@router.post("/login", response_model=TokenResponse)
def login_admin(form_data: OAuth2PasswordRequestForm = Depends(), session: Session = Depends(get_session)):
    return authenticate_admin(form_data, session)
