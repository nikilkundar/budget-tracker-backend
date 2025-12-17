from fastapi import FastAPI
from .database import Base, engine

from fastapi.middleware.cors import CORSMiddleware

#Import all models so SQLAlchemy knows them
import app.models.user
import app.models.expense

#Create tables if they don't exist
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Budget Tracker API",
    version="1.0.0"
)
#CORS CONFIG
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from .routers.user_router import router as user_router
from .routers.expenses import router as expenses_router
from app.routers.auth_router import router as auth_router
# Code to check working status of database
# from .database import engine
# with engine.connect() as conn:
#     print("Connected!")

# @app.get("/")
# def home():
#     return {"message": "Budget Tracker API is running 🚀"}

# Base.metadata.create_all(bind=engine)
app.include_router(user_router)
app.include_router(expenses_router)
app.include_router(auth_router)
