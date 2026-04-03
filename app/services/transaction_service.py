from app.models.transaction import Transaction
from app.extensions import db

def create_transaction(user_id, data):
    txn = Transaction(user_id=user_id, **data)
    db.session.add(txn)
    db.session.commit()
    return txn


def get_transactions(user_id, filters):
    query = Transaction.query.filter_by(user_id=user_id)

    if filters.get("type"):
        query = query.filter_by(type=filters.get("type"))

    if filters.get("category"):
        query = query.filter_by(category=filters.get("category"))

    return query.order_by(Transaction.date.desc()).all()


def update_transaction(txn, data):
    for key, value in data.items():
        setattr(txn, key, value)

    db.session.commit()
    return txn


def delete_transaction(txn):
    db.session.delete(txn)
    db.session.commit()