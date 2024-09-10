from flask import request, jsonify
from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_restx import Namespace, Resource, marshal_with

from peewee import DoesNotExist

from werkzeug.exceptions import Unauthorized

from app.enums.http_status import HttpStatus
from app.logger_setup import LoggerSetup
from app.schemas.retrievers.user_schema_retriever import UserSchemaRetriever
from app.services.user_services.user_auth_service import UserAuthService
from app.services.user_services.user_crud_service import UserCRUDService
from app.validators.user_validator import (
    UserValidator,
)

user_namespace = Namespace("Users", description="User operations")
user_schema_retriever = UserSchemaRetriever(user_namespace)


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


@user_namespace.route("/<int:user_id>")
class GetUserById(Resource):
    @user_namespace.doc(
        description="Retrieve any user's profile by user ID. Requires admin privileges."
    )
    @jwt_required()
    @user_namespace.response(
        HttpStatus.OK.value,
        "User profile retrieved successfully.",
        user_schema_retriever.retrieve("profile"),
    )
    @user_namespace.response(HttpStatus.NOT_FOUND.value, "User not found")
    @user_namespace.response(HttpStatus.UNAUTHORIZED.value, "Unauthorized")
    @user_namespace.response(HttpStatus.INTERNAL_SERVER_ERROR.value, "Server error")
    @marshal_with(user_schema_retriever.retrieve("profile"))
    def get(self, user_id):
        try:
            current_user_id = get_jwt_identity()
            current_user_profile = UserCRUDService.get_user(current_user_id)

            if not UserAuthService.check_if_admin(current_user_profile):
                return (
                    {"message": "Unauthorized. Only admins can access this endpoint."},
                    HttpStatus.UNAUTHORIZED.value,
                )

            user_profile = UserCRUDService.get_user(user_id)
            if user_profile is None:
                return (
                    {"message": "User not found"},
                    HttpStatus.NOT_FOUND.value,
                )
            return user_profile

        except DoesNotExist:
            return (
                {"message": "User not found"},
                HttpStatus.NOT_FOUND.value,
            )
        except Unauthorized as e:
            return (
                {"message": str(e)},
                HttpStatus.UNAUTHORIZED.value,
            )
        except Exception as e:
            LoggerSetup.get_logger("general").error(
                f"Internal server error while getting the user with ID:{user_id}, err : {e}"
            )
            return (
                {"message": f"Internal server error: {str(e)}"},
                HttpStatus.INTERNAL_SERVER_ERROR.value,
            )


@user_namespace.route("/<int:user_id>/status/")
class ToggleUserStatus(Resource):
    @user_namespace.doc(
        description="Toggle user's active status by user ID. Requires admin privileges."
    )
    @jwt_required()
    @user_namespace.response(
        HttpStatus.OK.value,
        "User status updated successfully.",
        user_schema_retriever.retrieve("toggle_status"),
    )
    @user_namespace.response(HttpStatus.NOT_FOUND.value, "User not found")
    @user_namespace.response(HttpStatus.UNAUTHORIZED.value, "Unauthorized")
    @user_namespace.response(HttpStatus.INTERNAL_SERVER_ERROR.value, "Server error")
    def put(self, user_id):
        try:
            current_user_id = get_jwt_identity()
            current_user_profile = UserCRUDService.get_user(current_user_id)

            if not UserAuthService.check_if_admin(current_user_profile):
                return (
                    {"message": "Unauthorized."},
                    HttpStatus.UNAUTHORIZED.value,
                )

            user_profile = UserCRUDService.get_user(user_id)

            new_status, message = UserCRUDService.toggle_active_status(user_profile)

            return {"message": message, "is_active": new_status}, HttpStatus.OK.value

        except DoesNotExist:
            return (
                {"message": "User not found"},
                HttpStatus.NOT_FOUND.value,
            )
        except Unauthorized as e:
            return (
                {"message": "Unauthorized."},
                HttpStatus.UNAUTHORIZED.value,
            )
        except Exception as e:
            LoggerSetup.get_logger("general").error(
                f"Internal server error while toggling user status with ID:{user_id}, err : {e}"
            )
            return (
                {"message": f"Internal server error: {str(e)}"},
                HttpStatus.INTERNAL_SERVER_ERROR.value,
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


@user_namespace.route("/change-password/<int:user_id>")
class AdminChangePassword(Resource):
    @user_namespace.doc(
        description="Allows admin to change the password for a specified user by user ID. Requires admin privileges."
    )
    @user_namespace.expect(
        user_schema_retriever.retrieve("admin_change_password"), validate=True
    )
    @jwt_required()
    @user_namespace.response(HttpStatus.OK.value, "Password changed successfully.")
    @user_namespace.response(HttpStatus.NOT_FOUND.value, "User not found.")
    @user_namespace.response(HttpStatus.UNAUTHORIZED.value, "Unauthorized.")
    @user_namespace.response(HttpStatus.INTERNAL_SERVER_ERROR.value, "Server error.")
    def put(self, user_id):
        current_user_id = get_jwt_identity()

        try:
            current_user = UserCRUDService.get_user(current_user_id)
            if not UserAuthService.check_if_admin(current_user):
                return {"message": "Unauthorized"}, HttpStatus.UNAUTHORIZED.value

            user = UserCRUDService.get_user(user_id)
            data = request.json
            UserAuthService.change_password(user, data.get("new_password"))

            return {"message": "Password changed successfully"}, HttpStatus.OK.value

        except DoesNotExist:
            return {"message": "User not found"}, HttpStatus.NOT_FOUND.value

        except Exception as e:
            return {
                "message": f"Internal server error: {str(e)}"
            }, HttpStatus.INTERNAL_SERVER_ERROR.value
