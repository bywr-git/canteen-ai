from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app import crud, schemas
from app.database import SessionLocal
from app.security import require_admin

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
    search: str | None = Query(default=None, max_length=100),
    category: str | None = Query(default=None, max_length=50),
    available_only: bool = True,
    db: Session = Depends(get_db)
):
    return crud.get_food_items(db, search=search, category=category, available_only=available_only)


@router.get('/{item_id}', response_model=schemas.FoodItem)
def read_food_item(item_id: int, db: Session = Depends(get_db)):
    food = crud.get_food_item(db, item_id)
    if not food:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Food item not found')
    return food


@router.post("/")
def create_food_item(
    food: schemas.FoodItemCreate,
    db: Session = Depends(get_db),
    _=Depends(require_admin)
):
    return crud.create_food_item(db, food)


@router.put('/{item_id}', response_model=schemas.FoodItem)
def update_food_item(item_id: int, food: schemas.FoodItemCreate, db: Session = Depends(get_db), _=Depends(require_admin)):
    updated = crud.update_food_item(db, item_id, food.model_dump())
    if not updated:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Food item not found')
    return updated


@router.delete('/{item_id}', status_code=204)
def delete_food_item(item_id: int, db: Session = Depends(get_db), _=Depends(require_admin)):
    if not crud.deactivate_food_item(db, item_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Food item not found')