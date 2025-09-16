from fastapi import APIRouter, Depends
from sqlmodel import Session
from app.database import get_session
from app.schemas import OrderCreate, OrderRead
from app.services.orders_service import create_order, list_all_orders

router = APIRouter(prefix="/orders", tags=["orders"])

@router.post("/", response_model=OrderRead)
def place_order(order_data: OrderCreate, session: Session= Depends(get_session)):
    return create_order(order_data, session)

@router.get("/", response_model=list[OrderRead])
def list_orders(session: Session = Depends(get_session)):
    return list_all_orders(session)

