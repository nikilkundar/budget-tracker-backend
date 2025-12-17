from pydantic import BaseModel, EmailStr

# Base shared fields
class UserBase(BaseModel):
    username: str
    email: EmailStr

# For user registration (includes password)
class UserCreate(UserBase):
    password: str

# What we return to the user (no password)
class UserResponse(UserBase):
    id: int

    class Config:
        orm_mode = True
