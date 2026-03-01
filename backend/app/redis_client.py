import redis
import os
import logging
from dotenv import load_dotenv

load_dotenv()

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")

# Connection pool for Redis
try:
    redis_client = redis.from_url(REDIS_URL, decode_responses=True)
    # Ping to check if connection is actually working
    redis_client.ping()
    REDIS_ENABLED = True
except Exception as e:
    logging.warning(f"Redis not available: {e}. Falling back to DB-only mode.")
    REDIS_ENABLED = False

def get_cached_url(short_code: str):
    if not REDIS_ENABLED:
        return None
    try:
        return redis_client.get(f"url:{short_code}")
    except Exception:
        return None

def set_cached_url(short_code: str, original_url: str, expire_seconds: int = 86400):
    # Cache for 24 hours by default
    if not REDIS_ENABLED:
        return
    try:
        redis_client.setex(f"url:{short_code}", expire_seconds, original_url)
    except Exception:
        pass
