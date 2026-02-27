# Vercel deployment checklist

## Why the function was crashing

- **Old deployment**: The error showed `main.py` line 8 as `create_all(bind=engine)`. In the fixed code, line 8 is `import database_models` and `create_all` runs only inside lifespan (and is skipped when `VERCEL` is set). So Vercel was still running a previous build.
- **localhost**: The log said "connection to server at localhost:5432" because the old code did not read `DATABASE_URL`; the fixed code uses `DATABASE_URL` from the environment.

## Steps to fix

1. **Set env vars in Vercel**  
   Project → **Settings** → **Environment Variables**  
   Add for **Production** (and Preview if you use it):
   - `DATABASE_URL` = `postgres://...@db.prisma.io:5432/postgres?sslmode=require`  
   (Use the value from the Prisma Postgres quickstart; do not commit it.)

2. **Deploy the fixed code**  
   - Commit and push all changes: `main.py`, `database.py`, `index.py`, `vercel.json`.
   - In Vercel, trigger a new deployment (e.g. push to the connected branch, or **Redeploy** with “Clear cache and redeploy” so the new code is used).

3. **Create the table in Prisma Postgres**  
   The app does not run `create_all` on Vercel. Create the `product` table once (e.g. via Prisma or SQL), or run migrations from your machine with `DATABASE_URL` set to the same URL.

## Why `vercel.json` had `{}`

An empty object is valid: Vercel auto-detects the app from `index.py` (or `app.py`). It was left minimal on purpose. You can add `buildCommand` / `installCommand` if you want the build to be explicit (as in the current `vercel.json`).
