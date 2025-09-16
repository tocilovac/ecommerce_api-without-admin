from sqlmodel import Session, select
from fastapi import HTTPException
from app.models import Product
from app.schemas import ProductCreate, ProductUpdate
from app.cache import get_cached_products, set_cached_products

def create_product(product: ProductCreate, session: Session):
    new_product = Product(**product.dict())
    session.add(new_product)
    session.commit()
    session.refresh(new_product)
    return new_product

def list_products(session: Session):
    cached= get_cached_products()
    if cached:
        return cached
    
    products = session.exec(select(Product)).all()
    set_cached_products(products)
    return products

def get_product_by_id(product_id: int, session: Session):
    product = session.get(Product, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

def update_product(product_id: int, product_update: ProductUpdate, session: Session):
    product = session.get(Product, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    update_data = product_update.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(product, key, value)

    session.add(product)
    session.commit()
    session.refresh(product)
    return product

def delete_product(product_id: int, session: Session):
    product = session.get(Product, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    session.delete(product)
    session.commit()


