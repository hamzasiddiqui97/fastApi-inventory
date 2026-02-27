# Vercel serverless: mount FastAPI app at /api so root can serve frontend.
from fastapi import FastAPI
from app.main import app as api_app

app = FastAPI()
app.mount("/api", api_app)
