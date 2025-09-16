from fastapi import APIRouter, Depends
from sqlmodel import Session
from app.database import get_session
from app.schemas import CartItemCreate, CartItemRead
from app.services.cart_service import (
    add_item_to_cart,
    get_user_cart,
    remove_item_from_cart
)

router = APIRouter(prefix="/cart", tags=["cart"])

@router.post("/", response_model=CartItemRead)
def add_to_cart(item: CartItemCreate, session: Session = Depends(get_session)):
    return add_item_to_cart(item, session)

@router.get("/", response_model=list[CartItemRead])
def get_cart(session: Session = Depends(get_session)):
    return get_user_cart(session)

@router.delete("/{item_id}")
def remove_from_cart(item_id: int, session: Session = Depends(get_session)):
    return remove_item_from_cart(item_id, session)
