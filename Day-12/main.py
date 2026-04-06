from fastapi import FastAPI
from sqlmodel import SQLModel
from database import engine
from routers.product import router

app = FastAPI()
app.include_router(router)


@app.on_event("startup")
def on_startup():
    SQLModel.metadata.create_all(engine)


@app.get("/")
def read_root():
    return {"message": "PostgreSQL connected!"}
