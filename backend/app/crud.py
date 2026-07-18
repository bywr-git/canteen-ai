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

def get_budgets(db: Session):
    return db.query(models.Budget).all()


def create_budget(
    db: Session,
    budget: schemas.BudgetCreate
):
    db_budget = models.Budget(
        **budget.model_dump()
    )

    db.add(db_budget)
    db.commit()
    db.refresh(db_budget)

    return db_budget

def get_budget_summary(db: Session, user_id: int):

    budget = (
        db.query(models.Budget)
        .filter(models.Budget.user_id == user_id)
        .first()
    )

    if not budget:
        return {
            "message": "Budget not found"
        }

    total_spent = (
        db.query(func.sum(models.Purchase.amount))
        .filter(models.Purchase.user_id == user_id)
        .scalar()
    )

    if total_spent is None:
        total_spent = 0

    remaining = float(budget.monthly_limit) - float(total_spent)

    if remaining > 0:
        status = "Within Budget"
    elif remaining == 0:
        status = "Budget Reached"
    else:
        status = "Over Budget"

    return {
        "user_id": user_id,
        "monthly_budget": float(budget.monthly_limit),
        "total_spent": float(total_spent),
        "remaining": remaining,
        "status": status
    }

def get_health_score(db: Session, user_id: int):

    purchases = (
        db.query(models.Purchase)
        .filter(models.Purchase.user_id == user_id)
        .all()
    )

    if not purchases:
        return {
            "message": "No purchases found."
        }

    healthy = 0
    junk = 0
    neutral = 0

    healthy_categories = [
        "Healthy",
        "Fruits",
        "Breakfast"
    ]

    junk_categories = [
        "Snacks",
        "Dessert"
    ]

    for purchase in purchases:

        food = (
            db.query(models.FoodItem)
            .filter(models.FoodItem.item_id == purchase.item_id)
            .first()
        )

        if not food:
            continue

        if food.category in healthy_categories:
            healthy += purchase.quantity

        elif food.category in junk_categories:
            junk += purchase.quantity

        else:
            neutral += purchase.quantity

    total = healthy + junk + neutral

    score = round((healthy / total) * 100, 2)

    if score >= 80:
        message = "Excellent eating habits!"
    elif score >= 60:
        message = "Good job! Try adding more fruits and healthy meals."
    elif score >= 40:
        message = "Average diet. Reduce snacks and desserts."
    else:
        message = "Your diet needs improvement."

    return {
        "user_id": user_id,
        "healthy_items": healthy,
        "junk_items": junk,
        "neutral_items": neutral,
        "healthy_score": score,
        "message": message
    }

def get_top_foods(db: Session, user_id: int):

    results = (
        db.query(
            models.FoodItem.name,
            models.FoodItem.category,
            func.count(models.Purchase.purchase_id).label("times_purchased")
        )
        .join(
            models.Purchase,
            models.FoodItem.item_id == models.Purchase.item_id
        )
        .filter(
            models.Purchase.user_id == user_id
        )
        .group_by(
            models.FoodItem.name,
            models.FoodItem.category
        )
        .order_by(
            func.count(models.Purchase.purchase_id).desc()
        )
        .limit(5)
        .all()
    )

    return [
        {
            "food_name": row.name,
            "category": row.category,
            "times_purchased": row.times_purchased
        }
        for row in results
    ]

def get_category_spending(db: Session, user_id: int):

    results = (
        db.query(
            models.FoodItem.category,
            func.sum(models.Purchase.amount).label("total_spent")
        )
        .join(
            models.Purchase,
            models.FoodItem.item_id == models.Purchase.item_id
        )
        .filter(
            models.Purchase.user_id == user_id
        )
        .group_by(
            models.FoodItem.category
        )
        .order_by(
            func.sum(models.Purchase.amount).desc()
        )
        .all()
    )

    return [
        {
            "category": row.category,
            "total_spent": float(row.total_spent)
        }
        for row in results
    ]

def get_nutrition_summary(db: Session, user_id: int):

    purchases = (
        db.query(models.Purchase)
        .filter(models.Purchase.user_id == user_id)
        .all()
    )

    if not purchases:
        return {
            "message": "No purchases found."
        }

    total_calories = 0
    total_protein = 0
    total_carbs = 0
    total_fat = 0
    total_sugar = 0

    for purchase in purchases:

        food = (
            db.query(models.FoodItem)
            .filter(models.FoodItem.item_id == purchase.item_id)
            .first()
        )

        if not food:
            continue

        total_calories += food.calories * purchase.quantity
        total_protein += food.protein * purchase.quantity
        total_carbs += food.carbs * purchase.quantity
        total_fat += food.fat * purchase.quantity
        total_sugar += food.sugar * purchase.quantity

    return {
        "user_id": user_id,
        "total_calories": total_calories,
        "protein": round(total_protein, 2),
        "carbs": round(total_carbs, 2),
        "fat": round(total_fat, 2),
        "sugar": round(total_sugar, 2)
    }