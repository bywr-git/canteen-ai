from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import timedelta

from .. import schemas, crud
from ..database import SessionLocal
from ..security import hash_password, verify_password, create_access_token, get_db

router = APIRouter(
    prefix="/auth",
    tags=["Auth"]
)


@router.post('/register', status_code=201)
def register(user: schemas.UserRegister, db: Session = Depends(get_db)):
    # Prevent admin creation via public registration
    existing = crud.get_user_by_email(db, user.email)
    if existing:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Registration failed")

    password_hash = hash_password(user.password)

    # Build a lightweight create object
    class _U:
        pass

    u = _U()
    u.name = user.name
    u.email = user.email
    u.department = user.department
    u.year = user.year
    u.password_hash = password_hash
    u.role = 'student'

    db_user = crud.create_user(db, u)

    return {
        "user": {
            "user_id": db_user.user_id,
            "name": db_user.name,
            "email": db_user.email,
            "role": db_user.role,
            "department": db_user.department,
            "year": db_user.year,
            "is_active": db_user.is_active
        }
    }


@router.post('/login')
def login(form_data: schemas.UserLogin, db: Session = Depends(get_db)):
    # Use constant-time responses: do not reveal existence
    user = crud.get_user_by_email(db, form_data.email)
    if not user or not user.password_hash:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    if not verify_password(form_data.password, user.password_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    # update last_login
    crud.update_user_last_login(db, user)

    access_token_expires = timedelta(minutes=60)
    token = create_access_token({"user_id": user.user_id, "role": user.role}, expires_delta=access_token_expires)

    return {
        "access_token": token,
        "token_type": "bearer",
        "user": {
            "user_id": user.user_id,
            "name": user.name,
            "email": user.email,
            "role": user.role,
            "department": user.department,
            "year": user.year,
            "is_active": user.is_active
        }
    }
