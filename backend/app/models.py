from sqlalchemy import (
    Column,
    Integer,
    String,
    TIMESTAMP,
    Boolean,
    Float,
    ForeignKey,
    text,
    Date
)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.types import JSON
from sqlalchemy.orm import relationship
from .database import Base

class User(Base):
    __tablename__ = "users"
    user_id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    password_hash = Column(String(512), nullable=True)
    role = Column(String(20), nullable=False, server_default=text("'student'"))
    department = Column(String(50), nullable=True)
    year = Column(Integer, nullable=True)
    is_active = Column(Boolean, nullable=False, server_default=text('TRUE'))

    created_at = Column(
        TIMESTAMP,
        server_default=text("CURRENT_TIMESTAMP")
    )

    updated_at = Column(
        TIMESTAMP,
        server_default=text("CURRENT_TIMESTAMP"),
        onupdate=text("CURRENT_TIMESTAMP")
    )

    last_login = Column(TIMESTAMP, nullable=True)

class FoodItem(Base):
    __tablename__ = "food_items"

    item_id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    category = Column(String, nullable=False)
    price = Column(Float, nullable=False)

    calories = Column(Integer, nullable=True)
    protein = Column(Float, nullable=True)
    carbs = Column(Float, nullable=True)
    fat = Column(Float, nullable=True)
    fiber = Column(Float, nullable=True)
    sugar = Column(Float, nullable=True)
    is_available = Column(Boolean, nullable=False, server_default=text('TRUE'))
    created_at = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"))
    updated_at = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"), onupdate=text("CURRENT_TIMESTAMP"))

class Purchase(Base):
    __tablename__ = "purchases"

    purchase_id = Column(Integer, primary_key=True, index=True)

    user_id = Column(
    Integer,
    ForeignKey("users.user_id")
    )

    item_id = Column(
    Integer,
    ForeignKey("food_items.item_id")
    )

    quantity = Column(Integer, nullable=False)
    unit_price = Column(Float, nullable=True)
    total_price = Column(Float, nullable=True)
    # Legacy amount is retained for compatibility with existing records/API clients.
    amount = Column(Float, nullable=True)
    notes = Column(String, nullable=True)

    purchase_time = Column(
        TIMESTAMP,
        server_default=text("CURRENT_TIMESTAMP")
    )

    purchased_at = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"))

class Budget(Base):
    __tablename__ = "budgets"

    budget_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(
    Integer,
    ForeignKey("users.user_id")
    )
    monthly_limit = Column(Float, nullable=False)
    period = Column(String(20), nullable=False, server_default=text("'monthly'"))
    start_date = Column(Date, nullable=True)
    end_date = Column(Date, nullable=True)
    created_at = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"))
    updated_at = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"), onupdate=text("CURRENT_TIMESTAMP"))


class FoodScan(Base):
    __tablename__ = "food_scans"

    scan_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False, index=True)
    image_reference = Column(String(500), nullable=True)
    detected_food_name = Column(String(255), nullable=True)
    confidence = Column(Float, nullable=True)
    estimated_calories = Column(Float, nullable=True)
    estimated_protein = Column(Float, nullable=True)
    estimated_carbohydrates = Column(Float, nullable=True)
    estimated_fat = Column(Float, nullable=True)
    estimated_fiber = Column(Float, nullable=True)
    portion_description = Column(String(500), nullable=True)
    analysis_notes = Column(String(2000), nullable=True)
    raw_analysis = Column(JSON().with_variant(JSONB, "postgresql"), nullable=True)
    status = Column(String(30), nullable=False, server_default=text("'pending_review'"))
    created_at = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"))
    updated_at = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"), onupdate=text("CURRENT_TIMESTAMP"))