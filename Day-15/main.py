from fastapi import FastAPI, Depends
from app.db.database import Base, engine
from app.routes import auth, product
from app.core.deps import get_current_user
app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(auth.router)
app.include_router(product.router)


@app.get("/")
def root():
    return {"msg": "API running"}


@app.get("/users/me")
def get_me(current_user=Depends(get_current_user)):
    return current_user
