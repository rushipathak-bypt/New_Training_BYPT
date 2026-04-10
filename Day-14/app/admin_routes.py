from fastapi import APIRouter, Depends
from sqlmodel import Session, select

from app.dependencies import get_admin_user
from app.database import get_session
from app.models import User

router = APIRouter(prefix="/admin")


@router.get("/users")
def get_users(session: Session = Depends(get_session), admin=Depends(get_admin_user)):
    return session.exec(select(User)).all()
