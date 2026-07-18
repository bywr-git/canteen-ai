from sqlalchemy import (
    Column,
    Integer,
    String,
    TIMESTAMP,
    Float,
    ForeignKey,
    text
)
from sqlalchemy.orm import relationship
from .database import Base

class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100))
    email = Column(String(100))
    department = Column(String(50))
    year = Column(Integer)

    created_at = Column(
        TIMESTAMP,
        server_default=text("CURRENT_TIMESTAMP")
    )

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