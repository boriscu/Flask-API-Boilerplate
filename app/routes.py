from flask import Flask
from flask_restx import Api
from .endpoints.user_endpoints import user_namespace


def init_app_routes(app: Flask) -> None:
    api = Api(
        app,
        version="1.0",
        title="API Documentation",
        description="A detailed description of the Flask API",
    )
    api.add_namespace(user_namespace, path="/user")

    from flask_jwt_extended import JWTManager

    jwt = JWTManager(app)
