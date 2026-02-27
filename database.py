import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Environment-aware: use DATABASE_URL on Vercel/production, fallback for local dev
db_url = os.environ.get(
    "DATABASE_URL",
    "postgresql://postgres:Siddiquiazmah@localhost:5432/fastapi",
)
if db_url.startswith("postgres://"):
    db_url = db_url.replace("postgres://", "postgresql://", 1)
# Serverless: short-lived connections, minimal pool to avoid "connection refused" and pool exhaustion
connect_args = {}
if db_url.startswith("postgresql://"):
    connect_args["connect_timeout"] = 10
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
