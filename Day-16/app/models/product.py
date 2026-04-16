from sqlalchemy import Column, Integer, String, ForeignKey
from app.db.database import Base


class Products(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    price = Column(Integer, nullable=False)
    description = Column(String)
    stock = Column(Integer, nullable=False)

    category_id = Column(Integer, ForeignKey("categories.id"))
