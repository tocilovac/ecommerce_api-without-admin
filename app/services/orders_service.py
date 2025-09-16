from sqlmodel import Session, select
from fastapi import HTTPException
from app.models import Order, CartItem, Product
from app.schemas import OrderCreate
from datetime import datetime

def create_order(order_data: OrderCreate, session: Session):
    cart_items = session.exec(
        select(CartItem).where(CartItem.user_id == order_data.user_id)
    ).all()

    if not cart_items:
        raise HTTPException(status_code=400, detail="Cart is empty")

    total = 0
    for item in cart_items:
        product = session.get(Product, item.product_id)
        if not product or product.stock < item.quantity:
            raise HTTPException(
                status_code=400,
                detail=f"Product {item.product_id} unavailable or out of stock"
            )
        total += product.price * item.quantity
        product.stock -= item.quantity
        session.add(product)

    order = Order(
        user_id=order_data.user_id,
        total_price=total,
        status="pending",
        created_at=datetime.utcnow()
    )
    session.add(order)
    session.commit()
    session.refresh(order)

    for item in cart_items:
        session.delete(item)
    session.commit()

    return order

def list_all_orders(session: Session):
    return session.exec(select(Order)).all()
