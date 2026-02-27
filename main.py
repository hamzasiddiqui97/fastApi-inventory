import os
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from products import Product
from database import session, engine
from sqlalchemy.orm import Session
import database_models

SEED_PRODUCTS = [
    Product(id=1, name="Product 1", description="Description 1", price=100, quantity=100),
]


def _run_create_all():
    """Create tables only in local dev. On Vercel do not run DDL; create tables via DB provider or migrations."""
    if os.environ.get("VERCEL"):
        return
    try:
        database_models.Base.metadata.create_all(bind=engine)
    except Exception:
        pass


def _seed_if_empty(db: Session):
    if os.environ.get("SEED_DB") != "1":
        return
    if db.query(database_models.Product).count() > 0:
        return
    for p in SEED_PRODUCTS:
        db.add(database_models.Product(**p.model_dump()))
    db.commit()


@asynccontextmanager
async def lifespan(app: FastAPI):
    _run_create_all()
    if not os.environ.get("VERCEL"):
        db = session()
        try:
            _seed_if_empty(db)
        finally:
            db.close()
    yield


app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


def get_db():
    db = session()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def read_root():
    return 'hello world'

    
@app.get("/products")
def get_all_products(db: Session = Depends(get_db)):
    return db.query(database_models.Product).all()


@app.get("/products/{product_id}")
def get_product(product_id: int,db:Session = Depends(get_db)):
    product = db.query(database_models.Product).filter(database_models.Product.id == product_id).first()
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


@app.post("/products")
def create_product(product: Product, db:Session = Depends(get_db)):
    db.add(database_models.Product(**product.model_dump()))
    db.commit()
    return product


@app.put("/products/{product_id}")
def update_product(product_id: int, product: Product, db:Session = Depends(get_db)):
    db_product = db.query(database_models.Product).filter(database_models.Product.id == product_id).first()
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    db_product.name = product.name
    db_product.description = product.description
    db_product.price = product.price
    db_product.quantity = product.quantity
    db.commit()
    return db_product


@app.delete("/products/{product_id}")
def delete_product(product_id: int, db:Session = Depends(get_db)):
    db_product = db.query(database_models.Product).filter(database_models.Product.id == product_id).first()
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    db.delete(db_product)
    db.commit()
    return {"message": "Product deleted successfully"}
    