from flask import Flask
from flask_restx import Api

from app.endpoints.user_endpoints import user_namespace
from app.endpoints.workspace_endpoints import workspace_namespace


def init_app_routes(app: Flask) -> None:
    authorizations = {
        "Bearer Auth": {
            "type": "apiKey",
            "in": "header",
            "name": "Authorization",
            "description": "Type in the *'Value'* input box below: **'Bearer &lt;JWT&gt;'**, where JWT is the token",
        },
    }

    api = Api(
        app,
        version="1.0",
        title="Flask Boilerplate API Documentation",
        description="A detailed description of the Flask API",
        authorizations=authorizations,
        security="Bearer Auth",
    )

    api.add_namespace(user_namespace, path="/api/v1/user")
    api.add_namespace(workspace_namespace, path="/api/v1/workspace")

    from flask_jwt_extended import JWTManager

    jwt = JWTManager(app)
