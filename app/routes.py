from flask import Flask
from .endpoints import user_endpoints


def init_app_routes(app: Flask) -> None:
    app.register_blueprint(user_endpoints.user_blueprint, url_prefix="/user")

    from flask_jwt_extended import JWTManager

    jwt = JWTManager(app)
