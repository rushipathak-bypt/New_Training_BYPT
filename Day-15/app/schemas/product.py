from pydantic import BaseModel


class ProductCreate(BaseModel):
    name: str
    description: str | None = None


class ProductResponse(BaseModel):
    id: int
    name: str
    description: str | None = None

    class Config:
        from_attributes = True
