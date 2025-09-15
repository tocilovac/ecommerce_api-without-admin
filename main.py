from fastapi import FastAPI
from fastapi.security import OAuth2PasswordBearer
from app.database import init_db
from app.routes import users, cart, orders
from app.routes.products import router as products_router
from app.routes.admin import router as admin_router

app = FastAPI(
    title="E-Commerce API",
    description="API for managing users, products, orders, and carts with role-based access.",
    version="1.0.0"
)

init_db()

# Include routers
app.include_router(users.router)
app.include_router(cart.router)
app.include_router(orders.router)
app.include_router(products_router, prefix="/products", tags=["products"])
app.include_router(admin_router)
