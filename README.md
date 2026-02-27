# FastAPI Inventory API

Backend API for product inventory. Runs locally or on Vercel (serverless) with PostgreSQL.

## Project structure

```
fast_api_basics/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI app, lifespan, CORS, router registration
│   ├── dependencies.py      # get_db (DB session)
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config.py        # Env: get_database_url, is_vercel, seed_db_enabled
│   │   └── database.py     # Engine, SessionLocal, session()
│   ├── models/              # SQLAlchemy ORM
│   │   ├── __init__.py
│   │   ├── base.py
│   │   └── product.py
│   ├── schemas/             # Pydantic request/response
│   │   ├── __init__.py
│   │   └── product.py
│   └── api/                 # Route handlers
│       ├── __init__.py
│       └── products.py      # /products CRUD
├── docs/
│   └── VERCEL_DEPLOY.md
├── index.py                 # Vercel entrypoint (from app.main import app)
├── requirements.txt
├── vercel.json
├── commands.txt             # Local run & curl examples
└── README.md
```

## Local run

```bash
# From project root; use a venv with dependencies installed
python -m uvicorn app.main:app --reload
```

API: `http://127.0.0.1:8000`  
Docs: `http://127.0.0.1:8000/docs`  
Products: `http://127.0.0.1:8000/products`

## Environment

- **DATABASE_URL**: PostgreSQL URL (optional locally; defaults to localhost).
- **SEED_DB=1**: Seed initial product when DB is empty (local only).
- On Vercel, set **DATABASE_URL** in project settings.

## Deploy (Vercel)

Push to the connected repo; Vercel builds and runs `index.py`. See `docs/VERCEL_DEPLOY.md`.
