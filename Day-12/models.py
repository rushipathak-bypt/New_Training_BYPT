from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from pydantic import BaseModel


class Category(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str

    products: List["Product"] = Relationship(back_populates="category")


class Product(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    price: float
    discount_percent: float = 0
    category_id: Optional[int] = Field(default=None, foreign_key="category.id")

    category: Optional[Category] = Relationship(back_populates="products")


class CategoryRead(BaseModel):
    id: int
    name: str


class ProductRead(BaseModel):
    id: int
    name: str
    price: float
    discount_percent: float
    category: Optional[CategoryRead]
