"""FastAPI application: lifespan, middleware, router registration."""
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import products_router
from app.core.config import is_vercel, seed_db_enabled
from app.core.database import engine, session
from app.models import Base, Product as ProductModel
from app.schemas import Product as ProductSchema

SEED_PRODUCTS = [
    ProductSchema(id=1, name="Product 1", description="Description 1", price=100.0, quantity=100),
]


def _run_create_all() -> None:
    try:
        Base.metadata.create_all(bind=engine)
    except Exception:
        pass


def _seed_if_empty(db) -> None:
    if not seed_db_enabled():
        return
    if db.query(ProductModel).count() > 0:
        return
    for p in SEED_PRODUCTS:
        db.add(ProductModel(**p.model_dump()))
    db.commit()


@asynccontextmanager
async def lifespan(app: FastAPI):
    _run_create_all()
    if not is_vercel():
        db = session()
        try:
            _seed_if_empty(db)
        finally:
            db.close()
    yield


app = FastAPI(title="FastAPI Inventory", lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(products_router, prefix="/products", tags=["products"])


@app.get("/")
def read_root():
    return "ok"
