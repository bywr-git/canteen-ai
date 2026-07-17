from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app import crud, schemas

router = APIRouter(
    prefix="/budgets",
    tags=["Budgets"]
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/")
def read_budgets(
    db: Session = Depends(get_db)
):
    return crud.get_budgets(db)


@router.post("/")
def create_budget(
    budget: schemas.BudgetCreate,
    db: Session = Depends(get_db)
):
    return crud.create_budget(db, budget)