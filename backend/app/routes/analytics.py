from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app import crud, schemas

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