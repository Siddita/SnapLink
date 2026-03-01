from sqlalchemy import Column, BigInteger, String, Text, DateTime, func
from .database import Base # You'll need to set up Base in database.py

class URL(Base):
    __tablename__ = "urls"

    id = Column(BigInteger, primary_key=True, index=True)
    original_url = Column(Text, nullable=False)
    short_code = Column(String(20), unique=True, index=True)
    created_at = Column(DateTime, server_default=func.now())
    expires_at = Column(DateTime, nullable=True)
    clicks = Column(BigInteger, default=0)
