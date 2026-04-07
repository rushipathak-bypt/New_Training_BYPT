from auth import hash_password, verify_password, create_access_token
from fastapi import APIRouter, Depends, HTTPException
from schemas import UserCreate, UserLogin
from database import get_session
from sqlmodel import Session, select
from models import User

router = APIRouter(prefix="/auth")


@router.post("/register")
def register(user: UserCreate, session: Session = Depends(get_session)):
    db_user = User(
        email=user.email,
        hashed_password=hash_password(user.password)
    )
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user


@router.post("/login")
def login(user: UserLogin, session: Session = Depends(get_session)):
    db_user = session.exec(
        select(User).where(User.email == user.email)).first()

    if not db_user or not verify_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=401, detail="Invaid Credentials")

    token = create_access_token({"sub": db_user.id})
    return {"access_token": token, "token_type": "bearer"}
