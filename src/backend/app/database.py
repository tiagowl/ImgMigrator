"""Database configuration and session management."""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.config import settings

# Normalize database URL to use psycopg3 if PostgreSQL
def normalize_database_url(url: str) -> str:
    """Normalize database URL to use psycopg3 driver for PostgreSQL."""
    if url.startswith("postgresql://") or url.startswith("postgres://"):
        # Replace postgresql:// or postgres:// with postgresql+psycopg:// for psycopg3
        if "postgresql+psycopg" not in url and "postgresql+psycopg2" not in url:
            url = url.replace("postgresql://", "postgresql+psycopg://", 1)
            url = url.replace("postgres://", "postgresql+psycopg://", 1)
    return url

# Create engine
database_url = normalize_database_url(settings.DATABASE_URL)
engine = create_engine(
    database_url,
    connect_args={"check_same_thread": False} if "sqlite" in database_url else {},
    echo=settings.DEBUG,
)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for models
Base = declarative_base()


def get_db():
    """Dependency for getting database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """Initialize database tables."""
    Base.metadata.create_all(bind=engine)






