from flask import request
from flask_jwt_extended import jwt_required
from flask_restx import Resource
from app.models.enums.http_status import HttpStatus
from app.services.workspace_user_invite_services.workspace_user_invite_repository import (
    WorkspaceUserInviteRepository,
)

from . import workspace_user_invite_namespace, workspace_user_invite_schema_retriever


@workspace_user_invite_namespace.route(
    "/workspace/<int:workspace_id>", methods=["POST"]
)
class WorkspaceInviteEndpoint(Resource):
    @workspace_user_invite_namespace.doc(description="Creates an invite.")
    @workspace_user_invite_namespace.expect(
        workspace_user_invite_schema_retriever.retrieve("invite_creation_request")
    )
    @workspace_user_invite_namespace.response(
        HttpStatus.CREATED.value,
        "Invite created successfully",
        model=workspace_user_invite_schema_retriever.retrieve(
            "invite_creation_response"
        ),
    )
    @workspace_user_invite_namespace.response(
        HttpStatus.UNAUTHORIZED.value, "Authentication is required"
    )
    @workspace_user_invite_namespace.response(
        HttpStatus.BAD_REQUEST.value,
        "The invited user is already a part of the specified workspace",
    )
    @workspace_user_invite_namespace.response(
        HttpStatus.CONFLICT.value,
        "The specified user role can't be of type Admin",
    )
    @workspace_user_invite_namespace.response(
        HttpStatus.FORBIDDEN.value,
        "The invitor does not have admin rights to the workspace",
    )
    @workspace_user_invite_namespace.response(
        HttpStatus.NOT_ACCEPTABLE.value, "Workspace is over the user limit"
    )
    @jwt_required()
    def post(self, workspace_id):
        return WorkspaceUserInviteRepository.create_workspace_user_invite(
            workspace_id, request.get_json()
        )
