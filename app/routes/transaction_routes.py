from flask import Blueprint, request
from flask_jwt_extended import get_jwt_identity
from app.schemas.transaction_schema import transaction_schema, transactions_schema
from app.services.transaction_service import create_transaction, get_transactions, update_transaction, delete_transaction
from app.models.transaction import Transaction
from app.utils.decorators import role_required

txn_bp = Blueprint("transactions", __name__)

# CREATE → analyst, admin
@txn_bp.route("/transactions", methods=["POST"])
@role_required(["analyst", "admin"])
def create():
    user_id = int(get_jwt_identity())

    try:
        data = transaction_schema.load(request.json)
    except Exception as e:
        return {"error": str(e)}, 400

    txn = create_transaction(user_id, data)
    return transaction_schema.dump(txn), 201


# GET → all roles
@txn_bp.route("/transactions", methods=["GET"])
@role_required(["viewer", "analyst", "admin"])
def get_all():
    user_id = int(get_jwt_identity())

    txns = get_transactions(user_id, request.args)
    return transactions_schema.dump(txns)


# UPDATE → admin only
@txn_bp.route("/transactions/<int:id>", methods=["PUT"])
@role_required(["admin"])
def update(id):
    user_id = int(get_jwt_identity())

    txn = Transaction.query.get_or_404(id)

    if txn.user_id != user_id:
        return {"error": "Unauthorized"}, 403

    data = request.json
    txn = update_transaction(txn, data)

    return transaction_schema.dump(txn)


# DELETE → admin only
@txn_bp.route("/transactions/<int:id>", methods=["DELETE"])
@role_required(["admin"])
def delete(id):
    user_id = int(get_jwt_identity())

    txn = Transaction.query.get_or_404(id)

    if txn.user_id != user_id:
        return {"error": "Unauthorized"}, 403

    delete_transaction(txn)
    return {"message": "Deleted successfully"}