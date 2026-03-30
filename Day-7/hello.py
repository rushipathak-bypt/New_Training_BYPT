from fastapi import APIRouter
from datetime import datetime

router = APIRouter()

start_time = datetime.now()


@router.get("/hello")
def hello():
    return "Hello, FastAPI"


@router.post("/echo")
def echo(data: dict):
    return data


@router.get("/health")
def health():
    uptime = datetime.now() - start_time
    return {"status": "ok", "version": "1.0.0", "uptime": str(uptime)}
