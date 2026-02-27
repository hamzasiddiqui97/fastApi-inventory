"""Product CRUD API routes."""
import logging
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from app.dependencies import get_db
from app.models.product import Product as ProductModel
from app.schemas.product import Product as ProductSchema

logger = logging.getLogger(__name__)
router = APIRouter()


@router.get("", response_model=list[ProductSchema])
def get_all_products(db: Session = Depends(get_db)):
    rows = db.query(ProductModel).all()
    return [ProductSchema.model_validate(r) for r in rows]


@router.get("/{product_id}", response_model=ProductSchema)
def get_product(product_id: int, db: Session = Depends(get_db)):
    row = db.query(ProductModel).filter(ProductModel.id == product_id).first()
    if row is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return ProductSchema.model_validate(row)


@router.post("", response_model=ProductSchema)
def create_product(product: ProductSchema, db: Session = Depends(get_db)):
    try:
        db_product = ProductModel(**product.model_dump())
        db.add(db_product)
        db.commit()
        db.refresh(db_product)
        return ProductSchema.model_validate(db_product)
    except SQLAlchemyError:
        db.rollback()
        logger.exception("Database error while creating product")
        raise HTTPException(status_code=500, detail="Database error")
    except Exception:
        db.rollback()
        logger.exception("Unexpected error")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.put("/{product_id}", response_model=ProductSchema)
def update_product(
    product_id: int,
    product: ProductSchema,
    db: Session = Depends(get_db),
):
    db_product = db.query(ProductModel).filter(ProductModel.id == product_id).first()
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    db_product.name = product.name
    db_product.description = product.description
    db_product.price = product.price
    db_product.quantity = product.quantity
    db.commit()
    db.refresh(db_product)
    return ProductSchema.model_validate(db_product)


@router.delete("/{product_id}")
def delete_product(product_id: int, db: Session = Depends(get_db)):
    db_product = db.query(ProductModel).filter(ProductModel.id == product_id).first()
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    db.delete(db_product)
    db.commit()
    return {"message": "Product deleted successfully"}
