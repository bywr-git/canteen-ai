from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ..database import SessionLocal
from .. import crud, schemas
from ..security import get_current_user, require_admin, get_db, verify_password, hash_password

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


def _get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/", response_model=list[schemas.UserResponse])
def read_users(
    db: Session = Depends(_get_db),
    _: any = Depends(require_admin)
):
    return crud.get_users(db)


@router.post("/", response_model=schemas.UserResponse)
def create_user(
    user: schemas.UserCreate,
    db: Session = Depends(_get_db),
    _: any = Depends(require_admin)
):
    # Public registration is handled by /auth/register; this legacy endpoint is admin-only.
    return crud.create_user(db, user)


@router.get('/me')
def read_current_user(current_user=Depends(get_current_user)):
    return {
        "user_id": current_user.user_id,
        "name": current_user.name,
        "email": current_user.email,
        "role": current_user.role,
        "department": current_user.department,
        "year": current_user.year,
        "is_active": current_user.is_active
    }


@router.put('/me')
def update_current_user(update: schemas.UserCreate, db: Session = Depends(_get_db), current_user=Depends(get_current_user)):
    # allow updating name/department/year
    user = crud.get_user(db, current_user.user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    user.name = update.name
    user.department = update.department
    user.year = update.year
    db.add(user)
    db.commit()
    db.refresh(user)
    return {
        "user_id": user.user_id,
        "name": user.name,
        "email": user.email,
        "role": user.role,
        "department": user.department,
        "year": user.year,
        "is_active": user.is_active
    }


@router.post('/me/change-password')
def change_password(data: dict, db: Session = Depends(_get_db), current_user=Depends(get_current_user)):
    # Expect: {"current_password": "...", "new_password": "..."}
    current = data.get('current_password')
    new = data.get('new_password')
    if not current or not new:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Missing password fields")
    user = crud.get_user(db, current_user.user_id)
    if not user or not user.password_hash:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Cannot change password")
    if not verify_password(current, user.password_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Current password incorrect")
    if len(new) < 8:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="New password too short")
    user = crud.set_user_password(db, user, hash_password(new))
    return {"success": True}