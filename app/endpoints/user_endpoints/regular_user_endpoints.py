from flask import request
from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_restx import Resource, marshal_with

from app.models.enums.http_status import HttpStatus

from app.helpers.http_response_generator import HttpResponseGenerator

from app.services.user_services.user_verification_service import (
    UserVerificationService,
)
from app.services.user_services.user_repository import UserRepository

from . import user_namespace, user_schema_retriever


@user_namespace.route("/get_myself", methods=["GET"])
class GetMyselfEndpoint(Resource):
    @user_namespace.doc(
        description="Retrieve the logged-in user's profile. Requires a valid JWT token.",
    )
    @user_namespace.response(
        HttpStatus.OK.value,
        "Profile retrieved",
        user_schema_retriever.retrieve("profile"),
    )
    @user_namespace.response(HttpStatus.NOT_FOUND.value, "User Not Found")
    @marshal_with(user_schema_retriever.retrieve("profile"))
    @jwt_required()
    def get(self):
        return UserRepository.get_single_user(user_id=get_jwt_identity())


@user_namespace.route("/verify", methods=["POST", "GET"])
class UserVerificationEndpoint(Resource):
    @user_namespace.expect(
        user_schema_retriever.retrieve("user_verification"), validate=True
    )
    @user_namespace.doc(description="Verifies the user account.")
    @user_namespace.response(
        HttpStatus.OK.value,
        "Users account verified.",
        user_schema_retriever.retrieve("verification_response"),
    )
    @user_namespace.response(HttpStatus.BAD_REQUEST.value, "Token not valid.")
    def post(self):
        return UserVerificationService.submit(request.json.get("token"))

    @user_namespace.doc(
        description="Re-sends the verification email to the user. This endpoint should be called if the user did not receive or accidentally deleted their initial verification email. Requires a valid JWT."
    )
    @user_namespace.response(
        HttpStatus.OK.value, "Verification email has been re-sent successfully."
    )
    @user_namespace.response(
        HttpStatus.BAD_REQUEST.value,
        "Cannot re-send verification email because the user is already verified.",
    )
    @user_namespace.response(
        HttpStatus.UNAUTHORIZED.value,
        "Unauthorized access attempt detected. You must be logged in to request a verification email re-send.",
    )
    @jwt_required()
    def get(self):
        UserVerificationService.re_request(int(get_jwt_identity()))

        return HttpResponseGenerator.generate_response(HttpStatus.OK)
