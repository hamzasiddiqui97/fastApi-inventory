# Vercel deployment

## Root = frontend, API = /api

- **Root (/)**: Serves the React app from `frontend/build` (built by `buildCommand` in `vercel.json`).
- **API (/api)**: Handled by `api/index.py`, which mounts the FastAPI app at `/api`. So use `/api/products`, `/api/docs`, etc.

## Environment variables

- **DATABASE_URL**: PostgreSQL connection string. Set in Vercel → Project → Settings → Environment Variables (Production / Preview).
- Do not set `installCommand` to `pip install`; Vercel uses `uv` (PEP 668).

## Build

- `vercel.json` sets `buildCommand` to build the frontend (`cd frontend && npm install && npm run build`) and `outputDirectory` to `frontend/build`.
- The Python API is in `api/index.py`; Vercel installs dependencies and runs it for requests to `/api/*`.

## Tables

- The app runs `create_all` at startup (lifespan), so the `product` table is created if missing.

## If you get 404 on /api/products

1. In Vercel → Project → **Settings** → **General**, set **Root Directory** to **.** (leave empty or `.`) so the repo root is used. If Root Directory is `frontend`, the `api/` folder is not seen and the API is not deployed.
2. Confirm `api/index.py` exists at the repo root (same level as `app/`, `frontend/`) and is committed.
