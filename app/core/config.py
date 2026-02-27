"""Application configuration from environment."""
import os


def get_database_url() -> str:
    url = os.environ.get(
        "DATABASE_URL",
        "postgresql://postgres:Siddiquiazmah@localhost:5432/fastapi",
    )
    if url.startswith("postgres://"):
        url = url.replace("postgres://", "postgresql://", 1)
    return url


def is_vercel() -> bool:
    return bool(os.environ.get("VERCEL"))


def seed_db_enabled() -> bool:
    return os.environ.get("SEED_DB") == "1"
