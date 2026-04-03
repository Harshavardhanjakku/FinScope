from flask import Flask
from flask_cors import CORS
from app.config.config import Config
from app.extensions import db, migrate, jwt
from app.routes.auth_routes import auth_bp
from app.routes.transaction_routes import txn_bp
from app.routes.analytics_routes import analytics_bp
from app.utils.response import success_response, error_response
import logging


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # ✅ Enable CORS
    CORS(app)

    # ✅ Initialize Extensions
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)

    # ✅ Register Blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(txn_bp)
    app.register_blueprint(analytics_bp)

    # ✅ Logging (Production Style)
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s"
    )

    # ✅ Root Route
    @app.route("/")
    def home():
        return success_response(
            message="FinScope Backend Running 🚀"
        )

    # ✅ Global Error Handlers
    @app.errorhandler(404)
    def not_found(e):
        return error_response("Resource not found", 404)

    @app.errorhandler(400)
    def bad_request(e):
        return error_response("Bad request", 400)

    @app.errorhandler(500)
    def server_error(e):
        return error_response("Internal server error", 500)

    return app