from fastapi import APIRouter, Depends, HTTPException, Query, status
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
    current_user=Depends(get_current_user),
    category: str | None = Query(default=None, max_length=50)
):
    # Admins can see all purchases
    if current_user.role == 'admin':
        return crud.get_purchases(db)
    # Students only see their own purchases
    return crud.get_purchases_for_user_filtered(db, current_user.user_id, category)


@router.get('/{purchase_id}', response_model=schemas.Purchase)
def read_purchase(purchase_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    purchase = crud.get_purchase(db, purchase_id)
    if not purchase or (current_user.role != 'admin' and purchase.user_id != current_user.user_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Purchase not found')
    return purchase


@router.post("/")
def create_purchase(
    purchase: schemas.PurchaseCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    food = crud.get_food_item(db, purchase.item_id)
    if not food:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Food item not found')
    if not food.is_available:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Food item is unavailable')
    data = purchase.model_dump(exclude_none=True)
    # Students cannot create purchases for other users
    if current_user.role != 'admin':
        data['user_id'] = current_user.user_id
    else:
        # Admin may create purchases for users but ensure user_id provided
        if not data.get('user_id'):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='user_id required')

    data['unit_price'] = float(food.price)
    data['total_price'] = data['unit_price'] * purchase.quantity
    data['amount'] = data['total_price']
    return crud.create_purchase_from_dict(db, data)


@router.put('/{purchase_id}', response_model=schemas.Purchase)
def update_purchase(purchase_id: int, update: schemas.PurchaseCreate, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    purchase = crud.get_purchase(db, purchase_id)
    if not purchase or (current_user.role != 'admin' and purchase.user_id != current_user.user_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Purchase not found')
    food = crud.get_food_item(db, update.item_id)
    if not food or not food.is_available:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Food item is unavailable')
    data = {'item_id': update.item_id, 'quantity': update.quantity, 'notes': update.notes}
    data['unit_price'] = float(food.price)
    data['total_price'] = data['unit_price'] * update.quantity
    data['amount'] = data['total_price']
    return crud.update_purchase(db, purchase, data)


@router.delete('/{purchase_id}', status_code=204)
def delete_purchase(purchase_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    purchase = crud.get_purchase(db, purchase_id)
    if not purchase or (current_user.role != 'admin' and purchase.user_id != current_user.user_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Purchase not found')
    crud.delete_purchase(db, purchase)