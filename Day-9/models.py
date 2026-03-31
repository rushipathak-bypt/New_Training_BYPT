from sqlmodel import SQLModel, Field
from typing import Optional


# Base class (shared fields)
class ProductBase(SQLModel):
    name: str
    price: float
    category: str
    stock: int


# DB model (table)
class Product(ProductBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)


# Create schema (input)
class ProductCreate(ProductBase):
    pass


# Read schema (response)
class ProductRead(ProductBase):
    id: int


# Update schema (partial update)
class ProductUpdate(SQLModel):
    name: Optional[str] = None
    price: Optional[float] = None
    category: Optional[str] = None
    stock: Optional[int] = None
