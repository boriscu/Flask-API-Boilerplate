from flask import Flask
from flask_restx import Api

from app.endpoints.user_endpoints import user_namespace
from app.endpoints.auth_endpoints import auth_namespace
from app.endpoints.workspace_endpoints import workspace_namespace
from app.endpoints.workspace_user_invite_endpoints import (
    workspace_user_invite_namespace,
)


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
        prefix="/api",
    )

    api.add_namespace(user_namespace, path="/v1/user")
    api.add_namespace(auth_namespace, path="/v1/auth")
    api.add_namespace(workspace_namespace, path="/v1/workspace")
    api.add_namespace(workspace_user_invite_namespace, path="/v1/invite")

    from flask_jwt_extended import JWTManager

    jwt = JWTManager(app)
