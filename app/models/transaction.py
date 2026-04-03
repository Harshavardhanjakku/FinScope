from app.extensions import db
from datetime import datetime

class Transaction(db.Model):
    __tablename__ = "transactions"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False, index=True)
    amount = db.Column(db.Float, nullable=False)
    type = db.Column(db.String(10), nullable=False)  # income / expense
    category = db.Column(db.String(50), index=True)
    date = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    notes = db.Column(db.String(255))