"""Product SQLAlchemy model."""
from sqlalchemy import Column, Float, Integer, String

from app.models.base import Base


class Product(Base):
    __tablename__ = "product"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String, index=True)
    price = Column(Float, index=True)
    quantity = Column(Integer, index=True)
