"""
Configuration management for Canteen AI backend.

Loads configuration from environment variables with sensible defaults
and proper error handling. Never hardcode secrets.
"""

import os
import sys
from functools import lru_cache
from pathlib import Path

from dotenv import load_dotenv


# Load the repository-root environment file without overriding explicit
# process environment variables. Secrets remain server-side only.
ROOT_ENV_FILE = Path(__file__).resolve().parents[2] / ".env"
load_dotenv(ROOT_ENV_FILE)


class Settings:
    """Application settings loaded from environment variables."""

    # Database Configuration
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL",
        "postgresql://user:password@localhost:5432/canteen_ai"
    )

    # JWT/Security Configuration
    SECRET_KEY: str = os.getenv(
        "SECRET_KEY",
        "dev-secret-key-change-in-production"
    )

    ALGORITHM: str = os.getenv(
        "ALGORITHM",
        "HS256"
    )

    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv(
        "ACCESS_TOKEN_EXPIRE_MINUTES",
        "60"
    ))

    # AI Configuration
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")
    GEMINI_MODEL: str = os.getenv("GEMINI_MODEL", "gemini-3.6-flash")

    # API Configuration
    DEBUG: bool = os.getenv("DEBUG", "False").lower() == "true"
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")

    # CORS Configuration
    ALLOWED_ORIGINS: list = os.getenv(
        "ALLOWED_ORIGINS",
        "http://localhost:5173,http://localhost:3000"
    ).split(",")

    def validate(self):
        """
        Validate critical configuration values.
        Logs warnings for issues that should be fixed.
        Only raises ValueError for production environment errors.
        """
        warnings = []
        errors = []

        # Check if using default DATABASE_URL
        if self.DATABASE_URL.startswith("postgresql://user:"):
            msg = (
                "DATABASE_URL not configured. Using default placeholder. "
                "Please set DATABASE_URL environment variable. "
                "See .env.example for format."
            )
            if self.ENVIRONMENT == "production":
                errors.append(msg)
            else:
                warnings.append(msg)

        # Warn about default SECRET_KEY in development
        if self.SECRET_KEY == "dev-secret-key-change-in-production":
            msg = "Using default SECRET_KEY. Change this in production."
            if self.ENVIRONMENT == "production":
                errors.append("SECRET_KEY must be changed in production.")
            else:
                warnings.append(msg)

        # Log warnings
        if warnings:
            for warning in warnings:
                print(f"⚠️  Warning: {warning}", file=sys.stderr)

        # Raise errors
        if errors:
            error_message = "Configuration Error:\n" + "\n".join(errors)
            print(error_message, file=sys.stderr)
            raise ValueError(error_message)

    def __repr__(self):
        db_safe = '***' if 'password' in self.DATABASE_URL else 'localhost'
        return (
            f"Settings(ENVIRONMENT={self.ENVIRONMENT}, "
            f"DATABASE_URL={db_safe})"
        )


@lru_cache()
def get_settings() -> Settings:
    """
    Get cached application settings.
    Uses @lru_cache to ensure settings are loaded only once.
    """
    settings = Settings()
    settings.validate()
    return settings


# Load settings when module is imported
# This ensures configuration is validated early
try:
    settings = get_settings()
except ValueError as e:
    print(f"❌ Failed to load configuration: {e}", file=sys.stderr)
    if os.getenv("ENVIRONMENT") == "production":
        sys.exit(1)
    else:
        # In development, allow startup with warnings
        # but database operations will fail if URL is wrong
        print("⚠️  Continuing in development mode with default settings", file=sys.stderr)
        settings = Settings()
