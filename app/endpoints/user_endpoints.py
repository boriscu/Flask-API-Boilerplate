from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from app.enums.http_status import HttpStatus
from app.services.user_services.user_auth_service import UserAuthService
from app.validators.user_validator import (
    UserValidator,
)

user_blueprint = Blueprint("user_endpoints", __name__)


@user_blueprint.route("/register/", methods=["POST"])
def register():
    """
    Endpoint to register a new user.

    Request body should contain:
    - name: str
    - surname: str
    - email: str
    - password: str
    """
    data = request.get_json()

    is_valid, message = UserValidator.validate_user_data(data)
    if not is_valid:
        return jsonify({"message": message}), HttpStatus.BAD_REQUEST.value

    message, status_code = UserAuthService.register(data)
    return jsonify(message), status_code


@user_blueprint.route("/login/", methods=["POST"])
def login():
    """
    Endpoint for user login.

    Request body should contain:
    - email: str
    - password: str
    """
    data = request.get_json()

    return UserAuthService.login(data)


@user_blueprint.route("/logout/", methods=["POST"])
@jwt_required()
def logout():
    """
    Endpoint for logging out the current user.
    Requires valid JWT token.
    """
    return UserAuthService.logout()
