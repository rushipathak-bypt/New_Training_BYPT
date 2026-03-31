from fastapi import FastAPI
from sqlmodel import SQLModel
from database import engine
from routers.product import router
from contextlib import asynccontextmanager
from dotenv import load_dotenv
import os

load_dotenv()


@asynccontextmanager
async def lifespan(app: FastAPI):
    # 🔹 Startup logic
    print("Starting app...")
    SQLModel.metadata.create_all(engine)

    yield


app = FastAPI(
    title=os.getenv("APP_NAME", "FastAPI App"),
    lifespan=lifespan
)

app.include_router(router)
