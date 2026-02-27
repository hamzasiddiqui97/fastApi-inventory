from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from products import Product
from database import session, engine
from sqlalchemy.orm import Session
import database_models

database_models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
)

products = [
    Product(id=1, name="Product 1", description="Description 1", price=100, quantity=100),
]


def init_db():
    db = session()

    count = db.query(database_models.Product).count()
    if count == 0:
        for product in products:
            db.add(database_models.Product(**product.model_dump()))
        db.commit()
    db.close()


init_db()


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
def get_all_products(db:Session = Depends(get_db)):


    db = next(get_db())
    products = db.query(database_models.Product).all()
    return products


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
    