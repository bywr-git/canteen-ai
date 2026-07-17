from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app import crud, schemas
from app.database import SessionLocal

router = APIRouter(
    prefix="/purchases",
    tags=["Purchases"]
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/")
def read_purchases(
    db: Session = Depends(get_db)
):
    return crud.get_purchases(db)


@router.post("/")
def create_purchase(
    purchase: schemas.PurchaseCreate,
    db: Session = Depends(get_db)
):
    return crud.create_purchase(db, purchase)