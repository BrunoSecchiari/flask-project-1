from flask import Flask, jsonify
from flask_jwt_extended import JWTManager
from flask_smorest import Api
import os

from blocklist import BLOCKLIST
from db import db
from resources.item import blp as ItemBlueprint
from resources.store import blp as StoreBlueprint
from resources.tag import blp as TagBlueprint
from resources.user import blp as UserBlueprint


def create_app(db_url=None):
    # Flask
    app = Flask(__name__)
    app.config["API_TITLE"] = "Flask - REST API"
    app.config["API_VERSION"] = "v1"
    app.config["OPENAPI_VERSION"] = "3.0.3"
    app.config["OPENAPI_URL_PREFIX"] = "/"
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
    app.config["OPENAPI_SWAGGER_UI_URL"] = (
        "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
    )
    app.config["PROPAGATE_EXCEPTIONS"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = db_url or os.getenv(
        "DATABASE_URL", "sqlite:///data.db"
    )
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # API
    api = Api(app)
    api.register_blueprint(ItemBlueprint)
    api.register_blueprint(StoreBlueprint)
    api.register_blueprint(TagBlueprint)
    api.register_blueprint(UserBlueprint)

    # DB
    db.init_app(app)

    with app.app_context():
        db.create_all()

    # JWT
    app.config["JWT_SECRET_KEY"] = "36529254799019018785978114458282420466"
    jwt = JWTManager(app)

    @jwt.additional_claims_loader
    def add_claims_to_jwt(identity):
        if identity == 1:
            return {"is_admin": True}

        return {"is_admin": False}

    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        return jsonify(
            {
                "status": 401,
                "error": "token_expired",
                "message": "The access token has expired.",
            }
        )

    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        return jsonify(
            {
                "status": 401,
                "error": "invalid_token",
                "message": "The access token is invalid.",
            }
        )

    @jwt.revoked_token_loader
    def revoked_token_callback(jwt_header, jwt_payload):
        return jsonify(
            {
                "status": 401,
                "error": "token_revoked",
                "message": "The access token has been revoked.",
            }
        )

    @jwt.token_in_blocklist_loader
    def check_if_token_in_blocklist(jwt_header, jwt_payload):
        return jwt_payload["jti"] in BLOCKLIST

    @jwt.unauthorized_loader
    def missing_token_callback(error):
        return jsonify(
            {
                "status": 401,
                "error": "authorization_required",
                "message": "The request does not contain an access token.",
            }
        )

    return app
