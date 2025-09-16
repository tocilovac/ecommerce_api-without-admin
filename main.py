from fastapi import FastAPI
from app.database import init_db
from app.routes.admin import router as admin_router
from app.routes.cart import router as cart_router
from app.routes.orders import router as orders_router
from app.routes.products import router as products_router
from app.routes.users import router as users_router

app = FastAPI(
    title="E-Commerce API",
    description="API for managing users, products, orders, and carts with role-based access.",
    version="1.0.0"
)

# Initialize database
init_db()

# Register routers
app.include_router(admin_router)
app.include_router(cart_router)
app.include_router(orders_router)
app.include_router(products_router)
app.include_router(users_router)
