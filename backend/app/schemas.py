from pydantic import BaseModel, HttpUrl
from datetime import datetime
from typing import Optional

# Base class: What data is common to both request and response?
class URLBase(BaseModel):
    original_url: HttpUrl  # Pydantic will auto-validate it's a valid http/https URL

# Request Schema: What do we need from the user to create a link?
class URLCreate(URLBase):
    expires_at: Optional[datetime] = None # Optional expiry date

# Response Schema: What do we send back to the user?
class URLResponse(URLBase):
    short_code: str
    created_at: datetime
    expires_at: Optional[datetime]
    clicks: int

    class Config:
        from_attributes = True  # Allows Pydantic to work with SQLAlchemy models
