from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from datetime import datetime
import os

from . import models, schemas, crud
from .database import engine, get_db
from .redis_client import get_cached_url, set_cached_url

# Create the tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="SnapLink API",
    description="A production-ready URL shortener service.",
    version="1.0.0"
)

# Enable CORS for frontend segregation
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # In production, replace with your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "SnapLink API is online. Use /shorten to create URLs or /stats for analytics."}

@app.post("/shorten", response_model=schemas.URLResponse)
def shorten_url(url_in: schemas.URLCreate, db: Session = Depends(get_db)):
    """
    Creates a new short URL and pre-caches it in Redis.
    """
    return crud.create_short_url(db=db, url_in=url_in)

@app.get("/stats/{short_code}", response_model=schemas.URLResponse)
def get_stats(short_code: str, db: Session = Depends(get_db)):
    """
    Get click counts and metadata for a short URL.
    """
    db_url = crud.get_url_stats(db, short_code)
    if not db_url:
        raise HTTPException(status_code=404, detail="Short URL not found")
    return db_url

@app.get("/{short_code}")
def redirect_to_url(short_code: str, db: Session = Depends(get_db)):
    """
    Redirects with Cache-Aside pattern and Expiry check.
    """
    # 1. Try Redis
    cached_url = get_cached_url(short_code)
    if cached_url:
        # For testing, we'll hit DB to increment click count.
        crud.increment_click(db, short_code)
        return RedirectResponse(url=cached_url)

    # 2. Database Fallback
    db_url = db.query(models.URL).filter(models.URL.short_code == short_code).first()
    
    if not db_url:
        raise HTTPException(status_code=404, detail="Short URL not found")

    # 3. Expiry Check
    if db_url.expires_at and db_url.expires_at < datetime.now():
        raise HTTPException(status_code=410, detail="This link has expired")
    
    # 4. Update Stats & Cache
    crud.increment_click(db, short_code)
    set_cached_url(short_code, db_url.original_url)
    
    return RedirectResponse(url=db_url.original_url)
