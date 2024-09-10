from flask import request, jsonify
from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_restx import Resource, marshal_with

from peewee import DoesNotExist

from app.enums.http_status import HttpStatus
from app.logger_setup import LoggerSetup
from app.services.user_services.user_auth_service import UserAuthService
from app.services.user_services.user_crud_service import UserCRUDService
from app.validators.user_validator import (
    UserValidator,
)
from . import user_namespace, user_schema_retriever


@user_namespace.route("/register/", methods=["POST"])
class Register(Resource):
    @user_namespace.doc(
        description="Register a new user. The request body must include name, surname, email, and password."
    )
    @user_namespace.expect(
        user_schema_retriever.retrieve("registration"), validate=True
    )
    @user_namespace.response(HttpStatus.CREATED.value, "User Registered")
    @user_namespace.response(HttpStatus.BAD_REQUEST.value, "Validation Error")
    @user_namespace.response(HttpStatus.INTERNAL_SERVER_ERROR.value, "Server Error")
    def post(self):
        data = request.get_json()

        is_valid, message = UserValidator.validate_user_register_data(data)
        if not is_valid:
            return jsonify({"message": message}), HttpStatus.BAD_REQUEST.value

        return UserAuthService.register(data)


@user_namespace.route("/login/", methods=["POST"])
class Login(Resource):
    @user_namespace.doc(description="Log in a user using their email and password.")
    @user_namespace.expect(user_schema_retriever.retrieve("login"), validate=True)
    @user_namespace.response(HttpStatus.OK.value, "Login Successful")
    @user_namespace.response(HttpStatus.UNAUTHORIZED.value, "Unauthorized")
    def post(self):
        data = request.get_json()

        is_valid, message = UserValidator.validate_user_login_data(data)
        if not is_valid:
            return jsonify({"message": message}), HttpStatus.BAD_REQUEST.value

        return UserAuthService.login(data)


@user_namespace.route("/logout/")
class Logout(Resource):
    @jwt_required()
    @user_namespace.doc(
        description="Log out the current user. Requires a valid JWT token."
    )
    @user_namespace.response(HttpStatus.OK.value, "Successfully logged out")
    @user_namespace.response(HttpStatus.UNAUTHORIZED.value, "Unauthorized")
    def post(self):
        return UserAuthService.logout()


@user_namespace.route("/get_myself/")
class GetMyself(Resource):
    @user_namespace.doc(
        description="Retrieve the logged-in user's profile. Requires a valid JWT token."
    )
    @jwt_required()
    @user_namespace.response(
        HttpStatus.OK.value,
        "Profile retrieved",
        user_schema_retriever.retrieve("profile"),
    )
    @user_namespace.response(HttpStatus.NOT_FOUND.value, "User Not Found")
    @user_namespace.response(HttpStatus.INTERNAL_SERVER_ERROR.value, "Server Error")
    @marshal_with(user_schema_retriever.retrieve("profile"))
    def get(self):
        try:
            current_user_id = get_jwt_identity()
            current_user_profile = UserCRUDService.get_user(current_user_id)

            return current_user_profile

        except DoesNotExist:
            return (
                {"message": "User not found"},
                HttpStatus.NOT_FOUND.value,
            )
        except Exception as e:
            LoggerSetup.get_logger("general").error(
                f"Internal server error while getting the user with ID:{current_user_id}, err : {e}"
            )
            return (
                {"message": f"Internal server error: {str(e)}"},
                HttpStatus.INTERNAL_SERVER_ERROR.value,
            )


@user_namespace.route("/check_auth/")
class CheckAuth(Resource):
    @user_namespace.doc(
        description="Check the validity of the current user's JWT token."
    )
    @jwt_required()
    @user_namespace.response(HttpStatus.OK.value, "Token is valid")
    @user_namespace.response(HttpStatus.UNAUTHORIZED.value, "Unauthorized")
    def get(self):
        try:
            get_jwt_identity()
            return {"message": "Token is valid"}, HttpStatus.OK.value
        except Exception:
            return {"message": "Unauthorized"}, HttpStatus.UNAUTHORIZED.value


@user_namespace.route("/check_admin/")
class CheckIfAdmin(Resource):
    @user_namespace.doc(description="Check if the current user is an Admin")
    @jwt_required()
    @user_namespace.response(
        HttpStatus.OK.value,
        "Checked if admin",
        user_schema_retriever.retrieve("is_admin"),
    )
    @user_namespace.response(HttpStatus.NOT_FOUND.value, "User Not Found")
    @user_namespace.response(HttpStatus.INTERNAL_SERVER_ERROR.value, "Server Error")
    @marshal_with(user_schema_retriever.retrieve("is_admin"))
    def get(self):
        try:
            current_user_id = get_jwt_identity()
            current_user_profile = UserCRUDService.get_user(current_user_id)
            return current_user_profile
        except DoesNotExist:
            return (
                {"message": "User not found"},
                HttpStatus.NOT_FOUND.value,
            )


@user_namespace.route("/check_active/")
class CheckIfActive(Resource):
    @user_namespace.doc(description="Check if the current user is an Active")
    @jwt_required()
    @user_namespace.response(
        HttpStatus.OK.value,
        "Checked if active",
        user_schema_retriever.retrieve("is_active"),
    )
    @user_namespace.response(HttpStatus.NOT_FOUND.value, "User Not Found")
    @user_namespace.response(HttpStatus.INTERNAL_SERVER_ERROR.value, "Server Error")
    @marshal_with(user_schema_retriever.retrieve("is_active"))
    def get(self):
        try:
            current_user_id = get_jwt_identity()
            current_user_profile = UserCRUDService.get_user(current_user_id)
            return current_user_profile
        except DoesNotExist:
            return (
                {"message": "User not found"},
                HttpStatus.NOT_FOUND.value,
            )


@user_namespace.route("/change-password")
class ChangePassword(Resource):
    @user_namespace.doc(
        description="Allows the current user to change their password. Requires authentication."
    )
    @jwt_required()
    @user_namespace.expect(
        user_schema_retriever.retrieve("change_password"), validate=True
    )
    @user_namespace.response(HttpStatus.OK.value, "Password changed successfully.")
    @user_namespace.response(HttpStatus.BAD_REQUEST.value, "Old password is incorrect.")
    @user_namespace.response(HttpStatus.NOT_FOUND.value, "User not found.")
    @user_namespace.response(HttpStatus.INTERNAL_SERVER_ERROR.value, "Server error.")
    def put(self):
        data = request.json
        user_id = get_jwt_identity()

        try:
            user = UserCRUDService.get_user(user_id)
            result = UserCRUDService.update_user_password(
                user, data.get("old_password"), data.get("new_password")
            )

            if result:
                return result, HttpStatus.BAD_REQUEST.value

            return {"message": "Password changed successfully"}, HttpStatus.OK.value

        except DoesNotExist:
            return {"message": "User not found"}, HttpStatus.NOT_FOUND.value

        except Exception as e:
            return {
                "message": f"Internal server error: {str(e)}"
            }, HttpStatus.INTERNAL_SERVER_ERROR.value
