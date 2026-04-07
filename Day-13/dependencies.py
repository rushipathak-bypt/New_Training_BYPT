from sqlmodel import Session
from jose import JWTError
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer

from database import get_session
from models import User
from auth import decode_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")


def get_current_user(
        token: str = Depends(oauth2_scheme),
        session: Session = Depends(get_session)):
    print("Token Received: ", token)
    try:
        payload = decode_token(token)
        print("PAYLOAD: ", payload)
        user_id: int = payload.get("sub")
        print("USER_ID: ", user_id)

    except Exception as e:
        print("JWT error: ", str(e))
        raise HTTPException(status_code=401, detail="Invalid token!!")

    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    return user


def get_admin_user(current_user: User = Depends(get_current_user)):
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Not Authorized")
    return current_user
