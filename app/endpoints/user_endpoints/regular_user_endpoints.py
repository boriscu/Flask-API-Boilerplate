from flask import request
from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_restx import Resource, marshal_with

from app.models.enums.http_status import HttpStatus

from app.helpers.http_response_generator import HttpResponseGenerator

from app.models.pg.user_profile import UserProfile
from app.services.user_services.user_auth_service import UserAuthService
from app.services.user_services.user_crud_service import UserCRUDService

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
    def post(self):
        data = request.get_json()
        return UserAuthService.register(data)


@user_namespace.route("/login/", methods=["POST"])
class Login(Resource):
    @user_namespace.doc(description="Log in a user using their email and password.")
    @user_namespace.expect(
        user_schema_retriever.retrieve("login_request"), validate=True
    )
    @user_namespace.response(
        HttpStatus.OK.value,
        "Login Successful",
        user_schema_retriever.retrieve("login_response"),
    )
    @user_namespace.response(HttpStatus.UNAUTHORIZED.value, "Unauthorized")
    def post(self):
        return UserAuthService.login(request.get_json())


@user_namespace.route("/get_myself/")
class GetMyself(Resource):
    @user_namespace.doc(
        description="Retrieve the logged-in user's profile. Requires a valid JWT token.",
    )
    @jwt_required()
    @user_namespace.response(
        HttpStatus.OK.value,
        "Profile retrieved",
        user_schema_retriever.retrieve("profile"),
    )
    @user_namespace.response(HttpStatus.NOT_FOUND.value, "User Not Found")
    @marshal_with(user_schema_retriever.retrieve("profile"))
    def get(self):
        return UserProfile.get_by_id(get_jwt_identity())


@user_namespace.route("/check_auth/")
class CheckAuth(Resource):
    @user_namespace.doc(
        description="Check the validity of the current user's JWT token."
    )
    @jwt_required()
    @user_namespace.response(HttpStatus.OK.value, "Token is valid")
    @user_namespace.response(HttpStatus.UNAUTHORIZED.value, "Unauthorized")
    def get(self):
        get_jwt_identity()
        return HttpResponseGenerator.generate_response(HttpStatus.OK)


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
    @user_namespace.response(HttpStatus.NOT_FOUND.value, "User not found.")
    def put(self):
        data = request.json

        user = UserProfile.get_by_id(int(get_jwt_identity()))

        result = UserCRUDService.update_user_password(
            user, data.get("old_password"), data.get("new_password")
        )

        if result:
            return result, HttpStatus.BAD_REQUEST.value

        return HttpResponseGenerator.generate_response(HttpStatus.OK)
