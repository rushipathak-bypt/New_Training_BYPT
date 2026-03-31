from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import select, Session
from typing import List, Optional
from models import Product, ProductCreate, ProductRead, ProductUpdate
from database import get_session

router = APIRouter(prefix="/products", tags=["Products"])


# POST PRODUCTS
@router.post("/", response_model=ProductCreate, status_code=201)
def create_product(product: Product, session: Session = Depends(get_session)):
    session.add(product)
    session.commit()
    session.refresh(product)
    return product


# GET PRODUCTS WITH FILTERS
@router.get("/", response_model=List[ProductRead])
def get_products(
    category: Optional[str] = None,
    min_price: Optional[float] = None,
    session: Session = Depends(get_session)
):
    query = select(Product)

    if category:
        query = query.where(Product.category == category)

    if min_price:
        query = query.where(Product.price >= min_price)

    return session.exec(query).all()


# GET PRODUCTS WITH ID
@router.get("/{id}", response_model=ProductRead)
def get_product(id: int, session: Session = Depends(get_session)):
    product = session.get(Product, id)

    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


# UPDATE PRODUCTS WITH ID
@router.put("/{id}", response_model=ProductUpdate)
def update_product(
    id: int, updated: Product,
    session: Session = Depends(get_session)
):
    product = session.get(Product, id)

    if not product:
        raise HTTPException(status_code=404, detail="Product Not Found!!")

    product.name = updated.name
    product.price = updated.price
    product.category = updated.category
    product.stock = updated.stock

    session.add(product)
    session.commit()
    session.refresh(product)

    return product


# DELETE PRODUCTS BY ID
@router.delete("/{id}")
def delete_product(id: int, session: Session = Depends(get_session)):
    product = session.get(Product, id)

    if not product:
        raise HTTPException(status_code=404, detail="Product Not Found!!")

    session.delete(product)
    session.commit()
    return {"message": "Product deleted successfully"}
