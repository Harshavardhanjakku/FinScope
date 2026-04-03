from flask import Blueprint
from flask_jwt_extended import get_jwt_identity
from app.services.analytics_service import (
    get_summary,
    get_category_breakdown,
    get_monthly_summary
)
from app.utils.decorators import role_required

analytics_bp = Blueprint("analytics", __name__)

# SUMMARY → all roles
@analytics_bp.route("/analytics/summary", methods=["GET"])
@role_required(["viewer", "analyst", "admin"])
def summary():
    user_id = int(get_jwt_identity())
    return get_summary(user_id)


# CATEGORY → analyst, admin
@analytics_bp.route("/analytics/category", methods=["GET"])
@role_required(["analyst", "admin"])
def category():
    user_id = int(get_jwt_identity())
    return {"data": get_category_breakdown(user_id)}


# MONTHLY → admin only
@analytics_bp.route("/analytics/monthly", methods=["GET"])
@role_required(["admin"])
def monthly():
    user_id = int(get_jwt_identity())
    return {"data": get_monthly_summary(user_id)}