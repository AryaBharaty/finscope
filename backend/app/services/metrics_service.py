import pandas as pd
from sqlalchemy.orm import Session
from backend.app.models.transaction import Transaction

def compute_financial_metrics(db: Session):
    transactions = db.query(Transaction).all()

    if not transactions:
        return {"message": "No transactions available"}

    df = pd.DataFrame([
        {"date": t.date, "amount": t.amount}
        for t in transactions
    ])

    df["date"] = pd.to_datetime(df["date"])
    df["month"] = df["date"].dt.to_period("M")

    monthly_income = (
        df[df.amount > 0]
        .groupby("month")["amount"]
        .sum()
    )

    monthly_expense = (
        df[df.amount < 0]
        .groupby("month")["amount"]
        .sum()
    )

    savings_rate = (
        (monthly_income + monthly_expense)
        .divide(monthly_income)
        .replace([float("inf"), -float("inf")], None)
        .dropna()
    ) * 100

    return {
        "monthly_income": monthly_income.astype(float).to_dict(),
        "monthly_expense": monthly_expense.astype(float).to_dict(),
        "savings_rate": savings_rate.astype(float).to_dict()
    }
