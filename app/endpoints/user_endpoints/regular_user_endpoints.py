from flask import request
from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_restx import Resource, marshal_with

from app.models.enums.http_status import HttpStatus

from app.helpers.http_response_generator import HttpResponseGenerator

from app.services.user_services.user_verification_service import (
    UserVerificationService,
)
from app.services.workspace_user_invite_services.workspace_non_registred_user_invite import (
    WorkspaceNonRegistredUserInviteService,
)

from app.services.user_services.user_repository import UserRepository

from . import user_namespace, user_schema_retriever


@user_namespace.route("/get_myself/", methods=["GET"])
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


@user_namespace.route("/verify", methods=["POST"])
class UserVerificationEndpoint(Resource):
    @user_namespace.expect(
        user_schema_retriever.retrieve("user_verification"), validate=True
    )
    @user_namespace.doc(description="Verifies the user account.")
    @user_namespace.response(HttpStatus.OK.value, "Users account verified.")
    @user_namespace.response(HttpStatus.BAD_REQUEST.value, "Token not valid.")
    def post(self):
        UserVerificationService.submit(request.json.get("token"))

        WorkspaceNonRegistredUserInviteService.invite_if_exists(
            request.json.get("email")
        )

        return HttpResponseGenerator.generate_response(HttpStatus.OK)
