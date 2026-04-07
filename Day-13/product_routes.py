from fastapi import APIRouter, Depends
from sqlmodel import Session

from database import get_session
from models import Product
from schemas import ProductCreate
from dependencies import get_current_user

router = APIRouter(prefix="/products")


@router.post("/")
def create_product(
    product: ProductCreate,
    session: Session = Depends(get_session),
    user=Depends(get_current_user)
):
    db_product = Product(**product.model_dump())
    session.add(db_product)
    session.commit()
    session.refresh(db_product)
    return db_product
