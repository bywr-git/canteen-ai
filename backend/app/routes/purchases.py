from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app import crud, schemas
from app.database import SessionLocal
from app.security import get_current_user, require_admin

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
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    # Admins can see all purchases
    if current_user.role == 'admin':
        return crud.get_purchases(db)
    # Students only see their own purchases
    return crud.get_purchases_for_user(db, current_user.user_id)


@router.post("/")
def create_purchase(
    purchase: schemas.PurchaseCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    data = purchase.model_dump()
    # Students cannot create purchases for other users
    if current_user.role != 'admin':
        data['user_id'] = current_user.user_id
    else:
        # Admin may create purchases for users but ensure user_id provided
        if not data.get('user_id'):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='user_id required')

    return crud.create_purchase_from_dict(db, data)