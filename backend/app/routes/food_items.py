from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app import crud, schemas
from app.database import SessionLocal

router = APIRouter(
    prefix="/food-items",
    tags=["Food Items"]
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/")
def read_food_items(
    db: Session = Depends(get_db)
):
    return crud.get_food_items(db)


@router.post("/")
def create_food_item(
    food: schemas.FoodItemCreate,
    db: Session = Depends(get_db)
):
    return crud.create_food_item(db, food)