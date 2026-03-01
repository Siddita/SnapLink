from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

load_dotenv()

# Step 1: Get URI from environment
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL")

# Step 2: Create the central connection engine
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Step 3: Create a workshop for database tasks (Session)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Step 4: Create the base for our models
Base = declarative_base()

# Step 5: The helper that FastAPI will use to inject DB access into routes
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
