from sqlalchemy.orm import Session
from ..models.user import User
from ..schemas.user_schema import UserCreate
from ..core.security import hash_password

def create_user(db: Session, user: UserCreate):
    print("PASSWORD BEFORE HASHING:", user.password, type(user.password))
    hashed_pw = hash_password(user.password)
    db_user = User(
        username=user.username,
        email=user.email,
        password=hashed_pw
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()

def get_user_by_username(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()

def get_user_by_id(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()
