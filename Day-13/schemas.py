from pydantic import BaseModel, Field


class UserCreate(BaseModel):
    email: str
    password: str = Field(max_length=72)


class Token(BaseModel):
    access_token: str
    token_type: str


class ProductCreate(BaseModel):
    name: str
    category_id: int


class UserLogin(BaseModel):
    email: str
    password: str
