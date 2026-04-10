from app.auth import hash_password, verify_password, create_access_token
from fastapi import APIRouter, Depends, HTTPException
from app.schemas import UserCreate
from app.database import get_session
from sqlmodel import Session, select
from app.models import User
from fastapi.security import OAuth2PasswordRequestForm
router = APIRouter(prefix="/auth")


@router.post("/register")
def register(user: UserCreate, session: Session = Depends(get_session)):
    db_user = User(
        email=user.email,
        hashed_password=hash_password(user.password),
        is_admin=True   # temporary for testing
    )
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user


@router.post("/login")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: Session = Depends(get_session)
):
    user = session.exec(
        select(User).where(User.email == form_data.username)
    ).first()

    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token({"sub": str(user.id)})

    return {
        "access_token": token,
        "token_type": "bearer"
    }
