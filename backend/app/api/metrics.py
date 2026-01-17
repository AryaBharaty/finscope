from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from backend.app.core.database import SessionLocal
from backend.app.models.transaction import Transaction
from sqlalchemy import func 


router = APIRouter()

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/metrics")
def get_metrics(db: Session = Depends(get_db)):
    try:
        # Total income and expense
        total_income = db.query(Transaction).filter(Transaction.amount > 0).with_entities(func.sum(Transaction.amount)).scalar() or 0
        total_expense = db.query(Transaction).filter(Transaction.amount < 0).with_entities(func.sum(Transaction.amount)).scalar() or 0

        # Count of transactions
        total_transactions = db.query(Transaction).count()

        return {
            "total_income": total_income,
            "total_expense": total_expense,
            "net_balance": total_income + total_expense,
            "total_transactions": total_transactions
        }
    except Exception as e:
        return {"error": str(e)}
