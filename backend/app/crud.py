from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import date, datetime, timedelta

from . import models, schemas
from .models import User


def get_users(db: Session):
    return db.query(User).all()


def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()


def get_user(db: Session, user_id: int):
    return db.query(User).filter(User.user_id == user_id).first()


def create_user(db: Session, user):
    # Accept either a UserCreate-like or object with optional password_hash/role
    db_user = User(
        name=getattr(user, 'name', None),
        email=getattr(user, 'email', None),
        department=getattr(user, 'department', None),
        year=getattr(user, 'year', None),
        password_hash=getattr(user, 'password_hash', None),
        role=getattr(user, 'role', 'student')
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user


def update_user_last_login(db: Session, user: User):
    user.last_login = func.now()
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def set_user_password(db: Session, user: User, password_hash: str):
    user.password_hash = password_hash
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def get_food_items(db: Session, search: str | None = None, category: str | None = None, available_only: bool = False):
    query = db.query(models.FoodItem)
    if search:
        query = query.filter(models.FoodItem.name.ilike(f"%{search}%"))
    if category:
        query = query.filter(models.FoodItem.category == category)
    if available_only:
        query = query.filter(models.FoodItem.is_available.is_(True))
    return query.order_by(models.FoodItem.name).all()


def get_food_item(db: Session, item_id: int):
    return db.query(models.FoodItem).filter(models.FoodItem.item_id == item_id).first()


def create_food_item(
    db: Session,
    food: schemas.FoodItemCreate
):
    db_food = models.FoodItem(**food.model_dump())

    db.add(db_food)
    db.commit()
    db.refresh(db_food)

    return db_food


def update_food_item(db: Session, item_id: int, data: dict):
    food = get_food_item(db, item_id)
    if not food:
        return None
    for key, value in data.items():
        setattr(food, key, value)
    db.commit()
    db.refresh(food)
    return food


def deactivate_food_item(db: Session, item_id: int):
    return update_food_item(db, item_id, {'is_available': False})

def get_purchases(db: Session):
    return db.query(models.Purchase).all()


def get_purchases_for_user(db: Session, user_id: int):
    return db.query(models.Purchase).filter(models.Purchase.user_id == user_id).all()


def get_purchase(db: Session, purchase_id: int):
    return db.query(models.Purchase).filter(models.Purchase.purchase_id == purchase_id).first()


def get_purchases_for_user_filtered(db: Session, user_id: int, category: str | None = None):
    query = db.query(models.Purchase).join(models.FoodItem, models.FoodItem.item_id == models.Purchase.item_id)
    query = query.filter(models.Purchase.user_id == user_id)
    if category:
        query = query.filter(models.FoodItem.category == category)
    return query.order_by(models.Purchase.purchased_at.desc()).all()


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


def create_purchase_from_dict(db: Session, data: dict):
    db_purchase = models.Purchase(**data)
    db.add(db_purchase)
    db.commit()
    db.refresh(db_purchase)
    return db_purchase


def update_purchase(db: Session, purchase: models.Purchase, data: dict):
    for key, value in data.items():
        setattr(purchase, key, value)
    db.commit()
    db.refresh(purchase)
    return purchase


def delete_purchase(db: Session, purchase: models.Purchase):
    db.delete(purchase)
    db.commit()

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


def get_budget(db: Session, budget_id: int):
    return db.query(models.Budget).filter(models.Budget.budget_id == budget_id).first()


def get_current_budget(db: Session, user_id: int):
    today = date.today()
    return (
        db.query(models.Budget)
        .filter(models.Budget.user_id == user_id)
        .filter((models.Budget.start_date.is_(None)) | (models.Budget.start_date <= today))
        .filter((models.Budget.end_date.is_(None)) | (models.Budget.end_date >= today))
        .order_by(models.Budget.created_at.desc())
        .first()
    )


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


def update_budget(db: Session, budget: models.Budget, data: dict):
    for key, value in data.items():
        setattr(budget, key, value)
    db.commit()
    db.refresh(budget)
    return budget


def get_budget_summary_for_period(db: Session, budget: models.Budget):
    start = budget.start_date or date.today().replace(day=1)
    end = budget.end_date or date.today()
    spent = db.query(func.coalesce(func.sum(models.Purchase.total_price), func.sum(models.Purchase.amount), 0)).filter(
        models.Purchase.user_id == budget.user_id,
        func.date(func.coalesce(models.Purchase.purchased_at, models.Purchase.purchase_time)) >= start,
        func.date(func.coalesce(models.Purchase.purchased_at, models.Purchase.purchase_time)) <= end,
    ).scalar() or 0
    amount = float(budget.monthly_limit or 0)
    spent = float(spent)
    remaining = amount - spent
    return {
        'budget_id': budget.budget_id,
        'user_id': budget.user_id,
        'amount': amount,
        'monthly_budget': amount,
        'spent': spent,
        'total_spent': spent,
        'remaining': remaining,
        'percentage_used': (spent / amount * 100) if amount else 0,
        'status': 'Over Budget' if remaining < 0 else ('Budget Reached' if remaining == 0 else 'Within Budget'),
    }


def get_analytics_summary(db: Session, user_id: int):
    today = date.today()
    week_start = today - timedelta(days=today.weekday())
    month_start = today.replace(day=1)
    purchases = db.query(models.Purchase).filter(models.Purchase.user_id == user_id).all()
    values = [(p, float(p.total_price if p.total_price is not None else p.amount or 0)) for p in purchases]
    def in_range(p, start):
        timestamp = p.purchased_at or p.purchase_time
        return timestamp is None or timestamp.date() >= start
    return {
        'user_id': user_id,
        'total_spending': sum(v for _, v in values),
        'spending_today': sum(v for p, v in values if in_range(p, today)),
        'spending_this_week': sum(v for p, v in values if in_range(p, week_start)),
        'spending_this_month': sum(v for p, v in values if in_range(p, month_start)),
        'number_of_purchases': len(values),
        'average_purchase_value': sum(v for _, v in values) / len(values) if values else 0,
    }


def get_spending_trend(db: Session, user_id: int):
    rows = db.query(
        func.date(func.coalesce(models.Purchase.purchased_at, models.Purchase.purchase_time)).label('day'),
        func.sum(func.coalesce(models.Purchase.total_price, models.Purchase.amount)).label('total')
    ).filter(models.Purchase.user_id == user_id).group_by('day').order_by('day').all()
    return [{'date': str(row.day), 'amount': float(row.total or 0)} for row in rows]

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


def create_food_scan(db: Session, data: dict):
    scan = models.FoodScan(**data)
    db.add(scan)
    db.commit()
    db.refresh(scan)
    return scan


def get_food_scan(db: Session, scan_id: int, user_id: int):
    return db.query(models.FoodScan).filter(
        models.FoodScan.scan_id == scan_id,
        models.FoodScan.user_id == user_id,
    ).first()


def get_food_scans(db: Session, user_id: int):
    return db.query(models.FoodScan).filter(
        models.FoodScan.user_id == user_id,
    ).order_by(models.FoodScan.created_at.desc()).all()


def update_food_scan(db: Session, scan: models.FoodScan, data: dict):
    for key, value in data.items():
        setattr(scan, key, value)
    db.commit()
    db.refresh(scan)
    return scan


def delete_food_scan(db: Session, scan: models.FoodScan):
    db.delete(scan)
    db.commit()