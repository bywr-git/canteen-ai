from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app import crud, schemas
from typing import List

router = APIRouter(
    prefix="/analytics",
    tags=["Analytics"]
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/monthly-spending")
def monthly_spending(
    db: Session = Depends(get_db)
):
    return crud.get_monthly_spending(db)

@router.get(
    "/budget-summary/{user_id}",
    response_model=schemas.BudgetSummaryResponse
)
def budget_summary(
    user_id: int,
    db: Session = Depends(get_db)
):
    return crud.get_budget_summary(db, user_id)

@router.get(
    "/health-score/{user_id}",
    response_model=schemas.HealthScoreResponse
)
def health_score(
    user_id: int,
    db: Session = Depends(get_db)
):
    return crud.get_health_score(db, user_id)


@router.get(
    "/top-foods/{user_id}",
    response_model=List[schemas.TopFood]
)
def top_foods(
    user_id: int,
    db: Session = Depends(get_db)
):
    return crud.get_top_foods(db, user_id)

@router.get(
    "/category-spending/{user_id}",
    response_model=List[schemas.CategorySpending]
)
def category_spending(
    user_id: int,
    db: Session = Depends(get_db)
):
    return crud.get_category_spending(db, user_id)

@router.get(
    "/nutrition-summary/{user_id}",
    response_model=schemas.NutritionSummary
)
def nutrition_summary(
    user_id: int,
    db: Session = Depends(get_db)
):
    return crud.get_nutrition_summary(db, user_id)