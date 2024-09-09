from flask import Blueprint, request, jsonify
from flask_jwt_extended import get_jwt_identity, jwt_required
from app.enums.http_status import HttpStatus
from app.logger_setup import LoggerSetup
from app.services.user_services.user_auth_service import UserAuthService
from app.services.user_services.user_crud_service import UserCRUDService
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


@user_blueprint.route("/get_myself/", methods=["GET"])
@jwt_required()
def get_myself():
    """
    Endpoint to retrieve the logged-in user's profile.
    Requires a valid JWT token and returns the user's profile excluding the password.
    """
    try:
        current_user_id = get_jwt_identity()
        user_profile = UserCRUDService.get_user(current_user_id)
        if user_profile:
            return jsonify(user_profile), HttpStatus.OK.value
        else:
            return jsonify({"message": "User not found"}), HttpStatus.NOT_FOUND.value
    except Exception as e:
        LoggerSetup.get_logger("general").error(
            f"Internal server error while getting the user with ID:{current_user_id}, err : {e}"
        )
        return jsonify({"message": str(e)}), HttpStatus.INTERNAL_SERVER_ERROR.value


@user_blueprint.route("/check_auth/", methods=["GET"])
@jwt_required()
def check_auth():
    """
    Checks if the provided JWT token is valid.
    """
    try:
        get_jwt_identity()
        return jsonify({"message": "Token is valid"}), HttpStatus.OK.value
    except Exception as e:
        return (
            jsonify({"message": "Invalid token", "error": str(e)}),
            HttpStatus.UNAUTHORIZED.value,
        )
