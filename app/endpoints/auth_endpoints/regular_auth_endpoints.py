from flask import make_response, request
from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_restx import Resource

from app.models.enums.http_status import HttpStatus

from app.models.pg.user_profile import UserProfile

from app.helpers.validators.password_validator import PasswordValidator
from app.helpers.http_response_generator import HttpResponseGenerator

from app.services.user_services.user_auth_service import UserAuthService
from app.services.user_services.user_password_reset_service import (
    UserPasswordResetService,
)
from app.services.user_services.user_repository import UserRepository

from . import auth_namespace, auth_schema_retriever


@auth_namespace.route("/register/", methods=["POST"])
class RegisterEndpoint(Resource):
    @auth_namespace.doc(
        description="Register a new user. Upon self-registration, users receive an access token for initial authorization, but their account remains inactive. Conversely, when an admin registers a user, the account is activated immediately, but no access token is provided."
    )
    @auth_namespace.expect(
        auth_schema_retriever.retrieve("registration"), validate=True
    )
    @auth_namespace.response(
        HttpStatus.CREATED.value,
        "User Registered",
        auth_schema_retriever.retrieve("login_response"),
    )
    @auth_namespace.response(
        HttpStatus.BAD_REQUEST.value, "Validation of one or more fields failed"
    )
    @auth_namespace.response(
        HttpStatus.FORBIDDEN.value, "User with that email already exists"
    )
    def post(self):
        access_token = UserAuthService.register(
            auth_schema_retriever.retrieve("registration").parse_args()
        )

        return make_response(
            {
                "msg": "User registered successfully",
                "access_token": access_token,
            },
            HttpStatus.CREATED.value,
        )


@auth_namespace.route("/", methods=["POST", "GET", "PUT"])
class BaseAuthEndpoint(Resource):
    @auth_namespace.doc(description="Log in using an  email and password.")
    @auth_namespace.expect(
        auth_schema_retriever.retrieve("login_request"), validate=True
    )
    @auth_namespace.response(
        HttpStatus.OK.value,
        "Login Successful",
        auth_schema_retriever.retrieve("login_response"),
    )
    @auth_namespace.response(HttpStatus.UNAUTHORIZED.value, "Unauthorized")
    def post(self):
        access_token = UserAuthService.login(request.get_json())
        if access_token:
            return make_response(
                {
                    "msg": "Login successful",
                    "access_token": access_token,
                },
                HttpStatus.OK.value,
            )
        else:
            return {"msg": "Password is incorrect"}, HttpStatus.UNAUTHORIZED.value

    @auth_namespace.doc(
        description="Check the validity of the current user's JWT token."
    )
    @auth_namespace.response(HttpStatus.OK.value, "Token is valid")
    @auth_namespace.response(HttpStatus.UNAUTHORIZED.value, "Unauthorized")
    @jwt_required()
    def get(self):
        get_jwt_identity()
        return HttpResponseGenerator.generate_response(HttpStatus.OK)

    @auth_namespace.doc(
        description="Allows the current user to change their password. Requires authentication."
    )
    @auth_namespace.expect(
        auth_schema_retriever.retrieve("change_password"), validate=True
    )
    @auth_namespace.response(HttpStatus.OK.value, "Password changed successfully.")
    @auth_namespace.response(HttpStatus.NOT_FOUND.value, "User not found.")
    @auth_namespace.response(HttpStatus.BAD_REQUEST.value, "Old password is incorrect.")
    @jwt_required()
    def put(self):
        data = request.json

        user = UserProfile.get_by_id(int(get_jwt_identity()))
        new_password = PasswordValidator.validate_password(data.get("new_password"))

        UserRepository.update_user_password(
            user, data.get("old_password"), new_password
        )

        return HttpResponseGenerator.generate_response(HttpStatus.OK)

    @auth_namespace.route("/password-reset-request/", methods=["POST"])
    class PasswordResetRequest(Resource):
        @auth_namespace.expect(
            auth_schema_retriever.retrieve("password_reset_request"), validate=True
        )
        @auth_namespace.doc(
            "Initiates a password reset process. An email with a reset link will be sent to the provided email address."
        )
        @auth_namespace.response(
            HttpStatus.OK.value, "Password reset email successfully sent."
        )
        @auth_namespace.response(HttpStatus.NOT_FOUND.value, "User not found.")
        def post(self):
            UserPasswordResetService.request(request.json.get("email"))

            return HttpResponseGenerator.generate_response(HttpStatus.OK)

    @auth_namespace.route("/password-reset-submit/", methods=["POST"])
    class PasswordResetRequest(Resource):
        @auth_namespace.expect(
            auth_schema_retriever.retrieve("password_reset_submit"), validate=True
        )
        @auth_namespace.doc(
            "Processes the submission of a password reset token and new password."
        )
        @auth_namespace.response(
            HttpStatus.OK.value, "Password has been successfully reset."
        )
        @auth_namespace.response(HttpStatus.UNAUTHORIZED.value, "Bad token.")
        def post(self):
            data = request.json
            password = PasswordValidator.validate_password(data.get("password"))

            UserPasswordResetService.submit(password, data.get("token"))

            return HttpResponseGenerator.generate_response(HttpStatus.OK)
