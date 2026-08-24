from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app import crud, schemas
from typing import List
from app.security import get_current_user

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
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    # Admin: full overview; Students: only their own aggregated spending
    if current_user.role == 'admin':
        return crud.get_monthly_spending(db)
    return [s for s in crud.get_monthly_spending(db) if s['user_id'] == current_user.user_id]


@router.get('/summary')
def summary(db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    return crud.get_analytics_summary(db, current_user.user_id)


@router.get('/spending')
def spending(db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    return crud.get_spending_trend(db, current_user.user_id)


@router.get('/categories')
def categories(db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    return crud.get_category_spending(db, current_user.user_id)

@router.get(
    "/budget-summary/{user_id}",
    response_model=schemas.BudgetSummaryResponse
)
def budget_summary(
    user_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    if current_user.role != 'admin' and user_id != current_user.user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Access denied')
    return crud.get_budget_summary(db, user_id)

@router.get(
    "/health-score/{user_id}",
    response_model=schemas.HealthScoreResponse
)
def health_score(
    user_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    if current_user.role != 'admin' and user_id != current_user.user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Access denied')
    return crud.get_health_score(db, user_id)


@router.get(
    "/top-foods/{user_id}",
    response_model=List[schemas.TopFood]
)
def top_foods(
    user_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    if current_user.role != 'admin' and user_id != current_user.user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Access denied')
    return crud.get_top_foods(db, user_id)

@router.get(
    "/category-spending/{user_id}",
    response_model=List[schemas.CategorySpending]
)
def category_spending(
    user_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    if current_user.role != 'admin' and user_id != current_user.user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Access denied')
    return crud.get_category_spending(db, user_id)

@router.get(
    "/nutrition-summary/{user_id}",
    response_model=schemas.NutritionSummary
)
def nutrition_summary(
    user_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    if current_user.role != 'admin' and user_id != current_user.user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Access denied')
    return crud.get_nutrition_summary(db, user_id)