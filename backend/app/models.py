from sqlalchemy import (
    Column,
    Integer,
    String,
    TIMESTAMP,
    Boolean,
    Float,
    ForeignKey,
    text
)
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
    name = Column(String)
    category = Column(String)
    price = Column(Float)

    calories = Column(Integer)
    protein = Column(Float)
    carbs = Column(Float)
    fat = Column(Float)
    sugar = Column(Float)

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

    quantity = Column(Integer)

    amount = Column(Float)

    purchase_time = Column(
        TIMESTAMP,
        server_default=text("CURRENT_TIMESTAMP")
    )

class Budget(Base):
    __tablename__ = "budgets"

    budget_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(
    Integer,
    ForeignKey("users.user_id")
    )
    monthly_limit = Column(Float)