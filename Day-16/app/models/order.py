from sqlalchemy import Integer, String, Column, ForeignKey, DateTime
from datetime import datetime
from app.db.database import Base


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))

    total_price = Column(Integer, nullable=False)
    status = Column(String, nullable=False)

    created_at = Column(DateTime, default=datetime.now())
