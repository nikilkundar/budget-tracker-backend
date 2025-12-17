from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..crud.user_crud import create_user, get_user_by_email
from ..schemas.user_schema import UserCreate, UserResponse

router = APIRouter(prefix="/users", tags=["Users"])

@router.post("/register", response_model=UserResponse)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    print("REQUEST BODY RECEIVED:", user)
    print("PASSWORD TYPE:", type(user.password))
    print("PASSWORD VALUE:", repr(user.password))
    # Check if email exists
    existing_user = get_user_by_email(db, user.email)
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    new_user = create_user(db, user)
    return new_user
