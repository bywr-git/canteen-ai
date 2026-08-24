from sqlalchemy import create_engine, inspect, text
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
else:
    # Additive, idempotent updates for existing PostgreSQL development data.
    # No tables are dropped or recreated.
    table_columns = {
        "users": {
            "password_hash": "VARCHAR(512)",
            "role": "VARCHAR(20) NOT NULL DEFAULT 'student'",
            "is_active": "BOOLEAN NOT NULL DEFAULT TRUE",
            "updated_at": "TIMESTAMP DEFAULT CURRENT_TIMESTAMP",
            "last_login": "TIMESTAMP",
        },
        "food_items": {
            "description": "VARCHAR(1000)", "fiber": "DOUBLE PRECISION",
            "is_available": "BOOLEAN NOT NULL DEFAULT TRUE",
            "created_at": "TIMESTAMP DEFAULT CURRENT_TIMESTAMP",
            "updated_at": "TIMESTAMP DEFAULT CURRENT_TIMESTAMP",
        },
        "purchases": {
            "unit_price": "DOUBLE PRECISION", "total_price": "DOUBLE PRECISION",
            "notes": "VARCHAR(500)", "purchased_at": "TIMESTAMP DEFAULT CURRENT_TIMESTAMP",
        },
        "budgets": {
            "period": "VARCHAR(20) NOT NULL DEFAULT 'monthly'",
            "start_date": "DATE", "end_date": "DATE",
            "created_at": "TIMESTAMP DEFAULT CURRENT_TIMESTAMP",
            "updated_at": "TIMESTAMP DEFAULT CURRENT_TIMESTAMP",
        },
    }
    from . import models  # noqa: E402

    inspector = inspect(engine)
    models.FoodScan.__table__.create(bind=engine, checkfirst=True)
    with engine.begin() as connection:
        for table_name, columns in table_columns.items():
            if not inspector.has_table(table_name):
                continue
            existing = {column["name"] for column in inspector.get_columns(table_name)}
            for column_name, column_definition in columns.items():
                if column_name not in existing:
                    connection.execute(text(
                        f"ALTER TABLE {table_name} ADD COLUMN {column_name} {column_definition}"
                    ))