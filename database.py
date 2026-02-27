import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


# Use DATABASE_URL environment variable if set (production), otherwise use local connection
db_url = os.environ.get(
    "DATABASE_URL",
    "postgresql://postgres:Siddiquiazmah@localhost:5432/fastapi"
)

engine = create_engine(db_url)
session = sessionmaker(bind=engine, autoflush=False, autocommit=False)
