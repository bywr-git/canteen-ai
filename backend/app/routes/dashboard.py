from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app import crud

router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"]
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/{user_id}")
def get_dashboard(
    user_id: int,
    db: Session = Depends(get_db)
):
    return {
        "budget": crud.get_budget_summary(db, user_id),
        "healthy_score": crud.get_health_score(db, user_id),
        "top_foods": crud.get_top_foods(db, user_id),
        "category_spending": crud.get_category_spending(db, user_id),
        "nutrition": crud.get_nutrition_summary(db, user_id)
    }