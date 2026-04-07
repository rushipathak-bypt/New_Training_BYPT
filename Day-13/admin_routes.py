from fastapi import APIRouter, Depends
from sqlmodel import Session, select

from dependencies import get_admin_user
from database import get_session
from models import User

router = APIRouter(prefix="/admin")


@router.get("/users")
def get_users(session: Session = Depends(get_session), admin=Depends(get_admin_user)):
    return session.exec(select(User)).all()
