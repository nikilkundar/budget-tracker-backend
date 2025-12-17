from fastapi import APIRouter, Depends, HTTPException, Query, Security
from sqlalchemy.orm import Session
from ..database import get_db
from ..schemas.expense_schema import ExpenseCreate, ExpenseResponse
from ..crud.expense_crud import create_expense, get_expenses_for_user, delete_expense, update_expense
from app.core.current_user import get_current_user
from app.schemas.expense_schema import ExpenseUpdate
from app.schemas.expense_schema import MonthlySummary
from app.crud.expense_crud import get_monthly_summary
from datetime import datetime
from app.schemas.expense_schema import CategorySummary
from app.crud.expense_crud import get_category_summary


router = APIRouter(prefix="/expenses", tags=["Expenses"])

@router.post("/", response_model=ExpenseResponse)
def add_expense(
    expense: ExpenseCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    # user ID comes from JWT token
    new = create_expense(db, expense, current_user.id)
    return new

@router.get("/", response_model=list[ExpenseResponse])
def list_expenses(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    return get_expenses_for_user(db, user_id=current_user.id)


@router.delete("/{expense_id}", response_model=ExpenseResponse)
def delete_expense_route(
    expense_id: int,
    db: Session = Depends(get_db),
    current_user = Security(get_current_user)
):
    result = delete_expense(db, expense_id, current_user.id)

    if result is None:
        raise HTTPException(status_code=404, detail="Expense not found")

    if result == "forbidden":
        raise HTTPException(status_code=403, detail="Not allowed to delete this expense")

    return result

@router.put("/{expense_id}", response_model=ExpenseResponse)
def update_expense_route(
    expense_id: int,
    update_data: ExpenseUpdate,
    db: Session = Depends(get_db),
    current_user = Security(get_current_user)
):
    result = update_expense(db, expense_id, update_data, current_user.id)

    if result is None:
        raise HTTPException(status_code=404, detail="Expense not found")

    if result == "forbidden":
        raise HTTPException(status_code=403, detail="Not allowed to update this expense")

    return result

@router.get("/summary/monthly", response_model=MonthlySummary)
def monthly_summary(
    db: Session = Depends(get_db),
    current_user = Security(get_current_user)
):
    total = get_monthly_summary(db, current_user.id)

    # Format month as YYYY-MM (example: 2025-02)
    month_str = datetime.utcnow().strftime("%Y-%m")

    return {
        "month": month_str,
        "total_spent": float(total)
    }


@router.get("/summary/categories", response_model=CategorySummary)
def category_summary(
    db: Session = Depends(get_db),
    current_user = Security(get_current_user)
):
    summary = get_category_summary(db, current_user.id)

    return {"summary": summary}