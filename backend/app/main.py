from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from sqlalchemy.exc import SQLAlchemyError
import logging

from .routes import users
from .routes import food_items
from .routes import purchases
from .routes import analytics
from .routes import budgets
from .routes import dashboard
from .config import settings

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Canteen AI API",
    version="0.1.0",
    description="AI-powered student food, budget, and habit tracker"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global exception handler for database errors
@app.exception_handler(SQLAlchemyError)
async def database_exception_handler(request: Request, exc: SQLAlchemyError):
    """
    Handle database errors without exposing internal details.
    Logs the full error server-side for debugging.
    """
    logger.error(f"Database error: {str(exc)}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "error": "A database error occurred. Please try again later.",
            "data": None
        }
    )

# Global exception handler for generic exceptions
@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    """
    Handle unexpected errors without exposing internal details.
    Logs the full error server-side for debugging.
    """
    logger.error(f"Unexpected error: {str(exc)}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "error": "An unexpected error occurred. Please try again later.",
            "data": None
        }
    )

app.include_router(users.router)
app.include_router(food_items.router)
app.include_router(purchases.router)
app.include_router(analytics.router)
app.include_router(budgets.router)
app.include_router(dashboard.router)

@app.get("/")
def home():
    """Health check endpoint."""
    return {
        "success": True,
        "message": "Canteen AI Backend Running",
        "environment": settings.ENVIRONMENT,
        "data": None
    }

@app.get("/health")
def health_check():
    """Simple health check endpoint."""
    return {
        "success": True,
        "message": "Backend is healthy",
        "data": None
    }