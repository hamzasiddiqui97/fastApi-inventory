# Vercel deployment

## Environment variables

- **DATABASE_URL**: PostgreSQL connection string (e.g. from Prisma Postgres). Set in Vercel → Project → Settings → Environment Variables for Production (and Preview if needed).
- Do not set `buildCommand`/`installCommand` to `pip install`; Vercel uses `uv` (PEP 668).

## Entrypoint

- Vercel runs `index.py`, which exports `app` from `app.main`.
- The app lives under `app/`; dependencies are installed from `requirements.txt` automatically.

## Tables

- The app runs `create_all` at startup (lifespan), so the `product` table is created if missing. No separate migration step required for this project.
