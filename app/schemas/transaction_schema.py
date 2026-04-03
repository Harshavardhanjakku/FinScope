from app.extensions import ma
from marshmallow import fields, validate

class TransactionSchema(ma.Schema):
    id = fields.Int(dump_only=True)
    amount = fields.Float(required=True)
    type = fields.Str(required=True, validate=validate.OneOf(["income", "expense"]))
    category = fields.Str(required=True)
    date = fields.DateTime()
    notes = fields.Str()

transaction_schema = TransactionSchema()
transactions_schema = TransactionSchema(many=True)