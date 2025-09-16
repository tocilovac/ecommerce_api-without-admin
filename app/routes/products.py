from fastapi import APIRouter, Depends, status
from sqlmodel import Session
from app.database import get_session
from app.schemas import ProductCreate, ProductRead, ProductUpdate
from app.dependencies import require_admin
from app.services.products_service import (
    create_product,
    list_products,
    get_product_by_id,
    update_product,
    delete_product
)

router = APIRouter(prefix="/products", tags=["products"])

@router.post("/", response_model=ProductRead, dependencies=[Depends(require_admin)])
def create_product(product: ProductCreate, session: Session = Depends(get_session)):
    return create_product(product, session)

@router.get("/", response_model=list[ProductRead])
def list_products(session: Session = Depends(get_session)):
    return list_products(session)

@router.get("/{product_id}", response_model=ProductRead)
def get_product(product_id: int, session: Session = Depends(get_session)):
    return get_product_by_id(product_id, session)

@router.put("/{product_id}", response_model=ProductRead, dependencies=[Depends(require_admin)])
def update_product(product_id: int, product_update: ProductUpdate, session: Session = Depends(get_session)):
    return update_product(product_id, product_update, session)

@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(require_admin)])
def delete_product(product_id: int, session: Session = Depends(get_session)):
    return delete_product(product_id, session)
