from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from database import get_session
from typing import List
from models import Category, CategoryUpdate, CategoryCreate, CategoryRead

router = APIRouter(prefix="/categories", tags=["Categories"])


# CREATE CATEGORY
@router.post("/", response_model=CategoryRead, status_code=201)
def create_category(
    cat: CategoryCreate,
    session: Session = Depends(get_session)
):
    existing = session.exec(
        select(Category).where(Category.slug == cat.slug)
    ).first()

    if existing:
        raise HTTPException(status_code=404, detail="Slug Already Exists!!!")

    db_cat = Category.model_validate(cat)
    session.add(db_cat)
    session.commit()
    session.refresh(db_cat)
    return db_cat


# READ ALL
@router.get("/", response_model=List[CategoryRead])
def get_categories(session: Session = Depends(get_session)):
    return session.exec(select(Category)).all()


# READ ONE
@router.get("/{id}", response_model=CategoryRead)
def get_category(id: int, session: Session = Depends(get_session)):
    cat = session.get(Category, id)

    if not cat:
        raise HTTPException(status_code=404, detail="Category Not Found!!!")
    return cat


# UPDATE
@router.put("/{id}", response_model=CategoryRead)
def update_category(id: int, updated: CategoryUpdate, session: Session = Depends(get_session)):
    cat = session.get(Category, id)
    if not cat:
        raise HTTPException(status_code=404, detail="Category Not Found!!!")

    update_data = updated.model_dump(exclude_unset=True)

    # Check duplicate slug if updating
    if "slug" in update_data:
        existing = session.exec(select(Category)).where(Category.slug == update_data["slug"]).first()

        if existing and existing.id != id:
            raise HTTPException(status_code=400, detail="Slug Already Exists!")

    for key, value in update_data.items():
        setattr(cat, key, value)

        session.add(cat)
        session.commit()
        session.refresh(cat)


@router.delete("/{id}")
def delete_category(id: int, session: Session = Depends(get_session)):
    cat = session.get(Category, id)
    if not cat:
        raise HTTPException(status_code=404, detail="Category Not Found")
    session.delete(cat)
    session.commit()
    return {"message": "Deleted successfully"}
