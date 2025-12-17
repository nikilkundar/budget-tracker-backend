from sqlalchemy.orm import Session
from ..models.expense import Expense
from ..schemas.expense_schema import ExpenseCreate
from decimal import Decimal
from datetime import datetime
from sqlalchemy import func

def create_expense(db: Session, expense: ExpenseCreate, user_id: int):
    amt = Decimal(str(expense.amount))
    db_expense = Expense(
        user_id=user_id,
        title=expense.title,
        amount=amt,
        category=expense.category,
        notes=expense.notes
    )
    db.add(db_expense)
    db.commit()
    db.refresh(db_expense)
    return db_expense


def get_expenses_for_user(db: Session, user_id: int, skip: int = 0, limit: int = 100):
    return db.query(Expense).filter(Expense.user_id == user_id).offset(skip).limit(limit).all()

def get_expense(db: Session, expense_id: int):
    return db.query(Expense).filter(Expense.id == expense_id).first()

def delete_expense(db: Session, expense_id: int, user_id: int):
    expense = db.query(Expense).filter(Expense.id == expense_id).first()

    if not expense:
        return None  # Expense not found

    # SECURITY: Only owner can delete
    if expense.user_id != user_id:
        return "forbidden"

    db.delete(expense)
    db.commit()
    return expense


def update_expense(db: Session, expense_id: int, update_data, user_id: int):
    expense = db.query(Expense).filter(Expense.id == expense_id).first()

    if not expense:
        return None

    if expense.user_id != user_id:
        return "forbidden"

    # Update only provided fields
    if update_data.title is not None:
        expense.title = update_data.title

    if update_data.amount is not None:
        expense.amount = Decimal(str(update_data.amount))

    if update_data.category is not None:
        expense.category = update_data.category

    if update_data.notes is not None:
        expense.notes = update_data.notes

    db.commit()
    db.refresh(expense)
    return expense


def get_monthly_summary(db: Session, user_id: int):
    # Get the first day of this month
    now = datetime.utcnow()
    start_of_month = datetime(now.year, now.month, 1)

    # Query total spent this month
    total = (
        db.query(func.sum(Expense.amount))
        .filter(Expense.user_id == user_id)
        .filter(Expense.created_at >= start_of_month)
        .scalar()
    )

    return total or 0


def get_category_summary(db: Session, user_id: int):
    results = (
        db.query(Expense.category, func.sum(Expense.amount))
        .filter(Expense.user_id == user_id)
        .group_by(Expense.category)
        .all()
    )

    # Convert list of tuples → dict
    summary = {category: float(total or 0) for category, total in results}

    return summary
