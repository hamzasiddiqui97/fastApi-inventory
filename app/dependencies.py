"""FastAPI dependencies (e.g. DB session)."""
from collections.abc import Generator
from fastapi import Depends
from sqlalchemy.orm import Session

from app.core.database import session


def get_db() -> Generator[Session, None, None]:
    db = session()
    try:
        yield db
    finally:
        db.close()
