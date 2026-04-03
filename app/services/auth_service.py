from app.models.user import User
from app.extensions import db
from app.utils.jwt import generate_token

def register_user(data):
    existing = User.query.filter_by(email=data["email"]).first()
    if existing:
        return None, "User already exists"

    user = User(email=data["email"], role=data.get("role", "viewer"))
    user.set_password(data["password"])

    db.session.add(user)
    db.session.commit()

    return user, None


def login_user(data):
    user = User.query.filter_by(email=data["email"]).first()

    if not user or not user.check_password(data["password"]):
        return None

    token = generate_token(user)
    return token