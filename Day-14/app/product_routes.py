from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from app.database import get_session
from app.models import Product, ProductCreate
from app.dependencies import get_current_user

router = APIRouter()


# ✅ CREATE PRODUCT (Protected)
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


# ✅ GET ALL PRODUCTS
@router.get("/")
def get_all_products(session: Session = Depends(get_session)):
    products = session.exec(select(Product)).all()
    return products


# ✅ GET PRODUCT BY ID
@router.get("/{product_id}")
def get_product(product_id: int, session: Session = Depends(get_session)):
    product = session.get(Product, product_id)

    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    return product


# ✅ UPDATE PRODUCT (Protected)
@router.put("/{product_id}")
def update_product(
    product_id: int,
    updated_data: Product,
    session: Session = Depends(get_session),
    user=Depends(get_current_user)
):
    product = session.get(Product, product_id)

    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    product.name = updated_data.name
    product.category_id = updated_data.category_id

    session.commit()
    session.refresh(product)

    return product


# ✅ DELETE PRODUCT (Protected)
@router.delete("/{product_id}")
def delete_product(
    product_id: int,
    session: Session = Depends(get_session),
    user=Depends(get_current_user)
):
    product = session.get(Product, product_id)

    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    session.delete(product)
    session.commit()

    return {"message": "Product deleted"}
