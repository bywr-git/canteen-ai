from sqlalchemy.orm import Session
from sqlalchemy import func

from . import models, schemas
from .models import User


def get_users(db: Session):
    return db.query(User).all()


def create_user(db: Session, user):
    db_user = User(
        name=user.name,
        email=user.email,
        department=user.department,
        year=user.year
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user


def get_food_items(db: Session):
    return db.query(models.FoodItem).all()


def create_food_item(
    db: Session,
    food: schemas.FoodItemCreate
):
    db_food = models.FoodItem(**food.model_dump())

    db.add(db_food)
    db.commit()
    db.refresh(db_food)

    return db_food

def get_purchases(db: Session):
    return db.query(models.Purchase).all()


def create_purchase(
    db: Session,
    purchase: schemas.PurchaseCreate
):
    db_purchase = models.Purchase(
        **purchase.model_dump()
    )

    db.add(db_purchase)
    db.commit()
    db.refresh(db_purchase)

    return db_purchase

def get_monthly_spending(db: Session):

    results = (
        db.query(
            models.Purchase.user_id,
            func.sum(models.Purchase.amount).label("total_spending")
        )
        .group_by(models.Purchase.user_id)
        .all()
    )

    return [
        {
            "user_id": row.user_id,
            "total_spending": float(row.total_spending)
        }
        for row in results
    ]