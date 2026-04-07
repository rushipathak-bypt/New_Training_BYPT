from fastapi import FastAPI
from sqlmodel import SQLModel
from database import engine
from routes import auth_routes, user_routes, admin_routes, product_routes
from sqlmodel import Session, select
from models import User
app = FastAPI()

SQLModel.metadata.create_all(engine)

app.include_router(auth_routes.router)
app.include_router(admin_routes.router)
app.include_router(product_routes.router)
app.include_router(user_routes.router)


with Session(engine) as session:
    user = session.exec(select(User).where(User.email == "rushi99@gmail.com")).first()
    user.is_admin = True
    session.add(user)
    session.commit()
