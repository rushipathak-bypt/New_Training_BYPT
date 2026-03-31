from pydantic import field_validator, BaseModel


class CreateProduct(BaseModel):
    name: str
    price: int
    category: str
    stock: int

    @field_validator("price")
    def validate_price(cls, value):
        if value <= 0:
            raise ValueError("Price must be greater than 0")
        return value


class ProductResponse(BaseModel):
    id: int
    name: str
    price: int
    category: str
    stock: int
