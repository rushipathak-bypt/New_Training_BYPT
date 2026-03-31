from fastapi import FastAPI, HTTPException
from models import CreateProduct, ProductResponse
from typing import List, Optional

app = FastAPI()

products = []
product_id_counter = 1


@app.post("/product", response_model=ProductResponse, status_code=201)
def create_product(product: CreateProduct):
    global product_id_counter

    new_product = product.model_dump()
    new_product["id"] = product_id_counter

    products.append(new_product)
    product_id_counter += 1

    return new_product


@app.get("/product/{id}", response_model=ProductResponse)
def get_product(id: int):
    for p in products:
        if p["id"] == id:
            return p
    raise HTTPException(status_code=404, detail="Product not found!!")


@app.get("/products", response_model=List[ProductResponse])
def get_products(category: Optional[str] = None, min_price: Optional[int] = None):
    result = products

    if category:
        result = [p for p in products if p["category"].lower() == category.lower()]

    if min_price:
        result = [p for p in products if p["price"] >= min_price]

    return result
