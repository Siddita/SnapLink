from sqlalchemy.orm import Session
from . import models, schemas
from .utils.hashid import encode_id
from .redis_client import set_cached_url

def create_short_url(db: Session, url_in: schemas.URLCreate):
    # 1. Create the initial record
    db_url = models.URL(
        original_url=str(url_in.original_url),
        expires_at=url_in.expires_at
    )
    db.add(db_url)
    db.flush() # Populates db_url.id

    # 2. Generate and update short code
    db_url.short_code = encode_id(db_url.id)
    
    db.commit()
    db.refresh(db_url)

    # 3. Pre-populate Redis for immediate high speed
    # We cache indefinitely if no expiry, or until expiry date
    set_cached_url(db_url.short_code, db_url.original_url)
    
    return db_url

def get_url_stats(db: Session, short_code: str):
    return db.query(models.URL).filter(models.URL.short_code == short_code).first()

def increment_click(db: Session, short_code: str):
    db_url = db.query(models.URL).filter(models.URL.short_code == short_code).first()
    if db_url:
        db_url.clicks += 1
        db.commit()
