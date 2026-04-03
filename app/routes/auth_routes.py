from flask import Blueprint, request, jsonify
from app.schemas.user_schema import user_schema
from app.services.auth_service import register_user, login_user

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/register", methods=["POST"])
def register():
    try:
        data = user_schema.load(request.json)
    except Exception as e:
        return {"error": str(e)}, 400

    user, error = register_user(data)

    if error:
        return {"error": error}, 400

    return {
        "message": "User registered successfully",
        "user": user_schema.dump(user)
    }, 201


@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.json

    token = login_user(data)

    if not token:
        return {"error": "Invalid credentials"}, 401

    return {
        "message": "Login successful",
        "token": token
    }