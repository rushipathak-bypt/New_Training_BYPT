from fastapi import FastAPI
from sqlmodel import SQLModel
from database import engine
from routers.category import router
from contextlib import asynccontextmanager


@asynccontextmanager
async def lifespan(app: FastAPI):
    SQLModel.metadata.create_all(engine)
    yield


app = FastAPI(lifespan=lifespan)

app.include_router(router)
