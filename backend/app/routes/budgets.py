from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app import crud, schemas
from app.security import get_current_user

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
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    if current_user.role == 'admin':
        return crud.get_budgets(db)
    # Return budgets for the current student
    return [b for b in crud.get_budgets(db) if b.user_id == current_user.user_id]


@router.get('/current')
def read_current_budget(db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    budget = crud.get_current_budget(db, current_user.user_id)
    if not budget:
        return {'budget': None, 'message': 'Budget not found'}
    return crud.get_budget_summary_for_period(db, budget)


@router.post("/")
def create_budget(
    budget: schemas.BudgetCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    data = budget.model_dump()
    if current_user.role != 'admin':
        data['user_id'] = current_user.user_id
    else:
        if not data.get('user_id'):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='user_id required')
    return crud.create_budget(db, schemas.BudgetCreate.model_validate(data))


@router.put('/{budget_id}')
def update_budget(budget_id: int, budget: schemas.BudgetCreate, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    existing = crud.get_budget(db, budget_id)
    if not existing or (current_user.role != 'admin' and existing.user_id != current_user.user_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Budget not found')
    data = budget.model_dump(exclude_none=True)
    if current_user.role != 'admin':
        data['user_id'] = current_user.user_id
    return crud.update_budget(db, existing, data)