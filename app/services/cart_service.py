from sqlmodel import Session, select
from fastapi import HTTPException
from app.models import CartItem, Product
from app.schemas import CartItemCreate

def add_item_to_cart(item: CartItemCreate, session: Session):
    product = session.get(Product, item.product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    cart_item = CartItem(**item.dict())
    session.add(cart_item)
    session.commit()
    session.refresh(cart_item)
    return cart_item

def get_user_cart(session: Session):
    cart_items = session.exec(select(CartItem)).all()
    return cart_items

def remove_item_from_cart(item_id: int, session: Session):
    item = session.get(CartItem, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Cart item not found")
    session.delete(item)
    session.commit()
    return {"detail": "Item removed from cart"}
