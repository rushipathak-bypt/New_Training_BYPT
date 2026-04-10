from fastapi import FastAPI
from sqlmodel import SQLModel
from app.database import engine
from app.routes import auth_routes, user_routes, admin_routes, product_routes
from app.routes.product_routes import router as product_router

app = FastAPI()

SQLModel.metadata.create_all(engine)

app.include_router(auth_routes.router)
app.include_router(admin_routes.router)
app.include_router(product_routes.router)
app.include_router(user_routes.router)
app.include_router(product_router, prefix="/products")
