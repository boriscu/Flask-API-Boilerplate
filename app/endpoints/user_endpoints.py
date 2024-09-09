from flask import request, jsonify
from flask_jwt_extended import get_jwt_identity, jwt_required
from app.enums.http_status import HttpStatus
from app.logger_setup import LoggerSetup
from app.schemas.retrievers.user_schema_retriever import UserSchemaRetriever
from app.services.user_services.user_auth_service import UserAuthService
from app.services.user_services.user_crud_service import UserCRUDService
from app.validators.user_validator import (
    UserValidator,
)
from flask_restx import Namespace, Resource

user_namespace = Namespace("users", description="User operations")
user_schema_retriever = UserSchemaRetriever(user_namespace)


@user_namespace.route("/register/", methods=["POST"])
class Register(Resource):
    @user_namespace.doc(
        description="Register a new user. The request body must include name, surname, email, and password."
    )
    @user_namespace.expect(
        user_schema_retriever.retrieve("registration"), validate=True
    )
    @user_namespace.response(201, "User Registered")
    @user_namespace.response(400, "Validation Error")
    @user_namespace.response(500, "Server Error")
    def post(self):
        data = request.get_json()

        is_valid, message = UserValidator.validate_user_register_data(data)
        if not is_valid:
            return jsonify({"message": message}), HttpStatus.BAD_REQUEST.value

        message, status_code = UserAuthService.register(data)
        return jsonify(message), status_code


@user_namespace.route("/login/", methods=["POST"])
class Login(Resource):
    @user_namespace.doc(description="Log in a user using their email and password.")
    @user_namespace.expect(user_schema_retriever.retrieve("login"), validate=True)
    @user_namespace.response(200, "Login Successful")
    @user_namespace.response(401, "Unauthorized")
    def login():
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
    @user_namespace.response(200, "Successfully logged out")
    @user_namespace.response(401, "Unauthorized")
    def post(self):
        return UserAuthService.logout()


@user_namespace.route("/get_myself/")
class GetMyself(Resource):
    @user_namespace.doc(
        description="Retrieve the logged-in user's profile. Requires a valid JWT token."
    )
    @jwt_required()
    @user_namespace.response(
        200, "Profile retrieved", user_schema_retriever.retrieve("profile")
    )
    @user_namespace.response(404, "User Not Found")
    @user_namespace.response(500, "Server Error")
    def get(self):
        try:
            current_user_id = get_jwt_identity()
            user_profile = UserCRUDService.get_user(current_user_id)
            if user_profile:
                return jsonify(user_profile), HttpStatus.OK.value
            else:
                return (
                    jsonify({"message": "User not found"}),
                    HttpStatus.NOT_FOUND.value,
                )
        except Exception as e:
            LoggerSetup.get_logger("general").error(
                f"Internal server error while getting the user with ID:{current_user_id}, err : {e}"
            )


@user_namespace.route("/check_auth/")
class CheckAuth(Resource):
    @user_namespace.doc(
        description="Check the validity of the current user's JWT token."
    )
    @jwt_required()
    @user_namespace.response(200, "Token is valid")
    @user_namespace.response(401, "Unauthorized")
    def get(self):
        try:
            get_jwt_identity()
            return jsonify({"message": "Token is valid"}), HttpStatus.OK.value
        except Exception as e:
            return (
                jsonify({"message": "Invalid token", "error": str(e)}),
                HttpStatus.UNAUTHORIZED.value,
            )
