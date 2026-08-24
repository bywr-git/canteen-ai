from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.pool import StaticPool

from .config import settings
import os
import sys

# Use TEST_DATABASE_URL if provided (tests may set this explicitly)
DATABASE_URL = os.getenv("TEST_DATABASE_URL") or settings.DATABASE_URL

# TESTING controls whether to allow SQLite usage for tests.
TESTING = os.getenv("TESTING", "False").lower() == "true"

# If not testing and DATABASE_URL is the development placeholder, fail loudly.
if not TESTING and isinstance(DATABASE_URL, str) and DATABASE_URL.startswith("postgresql://user:"):
    print("\nERROR: DATABASE_URL is not configured. Set DATABASE_URL to your Postgres connection string.\n", file=sys.stderr)
    raise RuntimeError("DATABASE_URL must be configured for development/production. To run tests locally, set TESTING=true.")

# For testing, prefer an in-memory SQLite database with a StaticPool so the
# same connection is reused across threads (works with TestClient).
if TESTING:
    DATABASE_URL = "sqlite:///:memory:"
    engine = create_engine(
        DATABASE_URL,
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
else:
    if settings.ENVIRONMENT == "production" and not DATABASE_URL.startswith("postgresql"):
        raise RuntimeError("Production requires a PostgreSQL DATABASE_URL.")
    engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()

# If testing, create tables automatically for the in-memory database.
if TESTING:
    from . import models  # noqa: E402
    Base.metadata.create_all(bind=engine)