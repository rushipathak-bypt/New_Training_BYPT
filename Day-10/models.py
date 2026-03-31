from sqlmodel import SQLModel, Field
from typing import Optional
from pydantic import field_validator


class CategoryBase(SQLModel):
    name: str
    description: Optional[str] = None
    slug: str

    @field_validator("slug")
    def check_slug(cls, v):
        if " " in v:
            raise ValueError("Slug must not contain any spaces")
        return v.lower()


class Category(CategoryBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)


class CategoryCreate(CategoryBase):
    pass


class CategoryRead(CategoryBase):
    id: int


class CategoryUpdate(SQLModel):
    name: Optional[str] = None
    description: Optional[str] = None
    slug: Optional[str] = None
