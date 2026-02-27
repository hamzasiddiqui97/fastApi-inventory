"""Database engine and session factory. Serverless-friendly pooling."""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import get_database_url

db_url = get_database_url()
connect_args = {"connect_timeout": 10} if db_url.startswith("postgresql://") else {}
engine = create_engine(
    db_url,
    pool_pre_ping=True,
    pool_size=1,
    max_overflow=0,
    connect_args=connect_args,
)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)


def session():
    return SessionLocal()
