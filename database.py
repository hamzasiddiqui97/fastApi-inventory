from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


db_url = "postgresql://postgres:Siddiquiazmah@localhost:5432/fastapi"
engine = create_engine(db_url)
session = sessionmaker(bind=engine,autoflush=False,autocommit=False)
