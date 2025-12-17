from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.auth_schema import LoginRequest, TokenResponse
from app.crud.user_crud import get_user_by_email
from app.core.security import verify_password
from app.core.auth import create_access_token

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/login", response_model=TokenResponse)
def login(request: LoginRequest, db: Session = Depends(get_db)):
    user = get_user_by_email(db, request.email)
    if not user:
        raise HTTPException(status_code=400, detail="Invalid email or password")

    if not verify_password(request.password, user.password):
        raise HTTPException(status_code=400, detail="Invalid email or password")

    token = create_access_token({"user_id": user.id})
    return {"access_token": token}
