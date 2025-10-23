from typing import Generator
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from .config import Settings
from sqlalchemy.orm import Session

settings = Settings() # type: ignore

# SQLAlchemy Base model
Base = declarative_base()

# Create engine
engine = create_engine(settings.DATABASE_URL, echo=False)

# Create session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Dependency for FastAPI
def get_db() ->  Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Helper for scripts / tools
def get_session() -> Session:
    """Get a standalone session for scripts or agents."""
    return SessionLocal()