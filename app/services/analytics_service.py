from app.models.transaction import Transaction
from app.extensions import db
from sqlalchemy import func


def get_summary(user_id):
    income = db.session.query(func.sum(Transaction.amount))\
        .filter(Transaction.user_id == user_id, Transaction.type == "income")\
        .scalar() or 0

    expense = db.session.query(func.sum(Transaction.amount))\
        .filter(Transaction.user_id == user_id, Transaction.type == "expense")\
        .scalar() or 0

    return {
        "total_income": float(income),
        "total_expense": float(expense),
        "balance": float(income - expense)
    }


def get_category_breakdown(user_id):
    results = db.session.query(
        Transaction.category,
        func.sum(Transaction.amount)
    ).filter(Transaction.user_id == user_id)\
     .group_by(Transaction.category).all()

    return [
        {"category": r[0], "total": float(r[1])}
        for r in results
    ]


def get_monthly_summary(user_id):
    results = db.session.query(
        func.date_trunc('month', Transaction.date),
        func.sum(Transaction.amount)
    ).filter(Transaction.user_id == user_id)\
     .group_by(func.date_trunc('month', Transaction.date))\
     .order_by(func.date_trunc('month', Transaction.date))\
     .all()

    return [
        {"month": str(r[0]), "total": float(r[1])}
        for r in results
    ]