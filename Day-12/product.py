from fastapi import APIRouter, Depends
from sqlmodel import Session, select
from sqlalchemy.orm import selectinload
from typing import List
from models import Product, Category, ProductRead
from database import get_session

router = APIRouter()

# ------------------ CATEGORY ------------------


@router.post("/categories")
def create_category(category: Category, session: Session = Depends(get_session)):
    session.add(category)
    session.commit()
    session.refresh(category)
    return category


@router.get("/categories", response_model=List[Category])
def get_categories(session: Session = Depends(get_session)):
    return session.exec(select(Category)).all()


# ------------------ PRODUCT ------------------

@router.post("/products")
def create_product(product: Product, session: Session = Depends(get_session)):
    session.add(product)
    session.commit()
    session.refresh(product)
    return product


@router.get("/products", response_model=list[ProductRead])
def get_products(session: Session = Depends(get_session)):
    statement = select(Product).options(selectinload(Product.category))
    return session.exec(statement).all()
