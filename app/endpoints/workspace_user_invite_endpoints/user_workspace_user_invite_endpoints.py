from flask import request
from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_restx import Resource, marshal_with

from app.models.enums.http_status import HttpStatus
from app.services.workspace_user_invite_services.workspace_user_invite_repository import (
    WorkspaceUserInviteRepository,
)

from . import workspace_user_invite_namespace, workspace_user_invite_schema_retriever


@workspace_user_invite_namespace.route("/<int:workspace_id>", methods=["POST"])
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
        invitor_id = int(get_jwt_identity())
        return WorkspaceUserInviteRepository.create_workspace_user_invite(
            workspace_id=workspace_id, invitor_id=invitor_id, data=request.get_json()
        )


@workspace_user_invite_namespace.route("/", methods=["GET", "PUT"])
class BaseUserWorkspaceEndpoint(Resource):
    @workspace_user_invite_namespace.doc(
        description="Fetches all invites with pagination, sorting, and filtering. In most cases you would use the filter to show only pending invites"
    )
    @workspace_user_invite_namespace.expect(
        workspace_user_invite_schema_retriever.retrieve("pagination_parser"),
        validate=True,
    )
    @workspace_user_invite_namespace.response(
        HttpStatus.OK.value,
        "Workspaces fetched successfully.",
        model=workspace_user_invite_schema_retriever.retrieve("invites"),
    )
    @workspace_user_invite_namespace.response(
        HttpStatus.UNAUTHORIZED.value, "Unauthorized."
    )
    @marshal_with(workspace_user_invite_schema_retriever.retrieve("invites"))
    @jwt_required()
    def get(self):
        args = workspace_user_invite_schema_retriever.retrieve(
            "pagination_parser"
        ).parse_args()
        invites, total_entries, total_pages = (
            WorkspaceUserInviteRepository.get_all_invites(args)
        )
        return {
            "invites": invites,
            "total_entries": total_entries,
            "total_pages": total_pages,
        }, HttpStatus.OK.value

    @workspace_user_invite_namespace.expect(
        workspace_user_invite_schema_retriever.retrieve("invite_accept_by_token"),
        validate=True,
    )
    @workspace_user_invite_namespace.doc(
        description="Accepts an invite through token sent from mail."
    )
    @workspace_user_invite_namespace.response(
        HttpStatus.OK.value,
        "Invite accepted successfully",
    )
    @workspace_user_invite_namespace.response(
        HttpStatus.NOT_FOUND.value, "Invite not found or expired."
    )
    @workspace_user_invite_namespace.response(
        HttpStatus.UNAUTHORIZED.value, "Authentication is required"
    )
    @jwt_required()
    def put(self):
        return WorkspaceUserInviteRepository.accept_user_invite_by_token(
            request.get_json()
        )


@workspace_user_invite_namespace.route("/<int:invite_id>", methods=["DELETE", "PUT"])
class SingleInviteEndpoint(Resource):
    @workspace_user_invite_namespace.doc(description="Declines an invite.")
    @workspace_user_invite_namespace.response(
        HttpStatus.OK.value,
        "Invite declined successfully",
    )
    @workspace_user_invite_namespace.response(
        HttpStatus.UNAUTHORIZED.value, "Authentication is required"
    )
    @jwt_required()
    def delete(self, invite_id):
        return WorkspaceUserInviteRepository.decline_user_invite(invite_id)

    @workspace_user_invite_namespace.doc(
        description="Accepts an invite through invite id."
    )
    @workspace_user_invite_namespace.response(
        HttpStatus.OK.value,
        "Invite accepted successfully",
    )
    @workspace_user_invite_namespace.response(
        HttpStatus.NOT_FOUND.value, "Invite not found."
    )
    @workspace_user_invite_namespace.response(
        HttpStatus.UNAUTHORIZED.value, "Authentication is required"
    )
    @jwt_required()
    def put(self, invite_id):
        return WorkspaceUserInviteRepository.accept_user_invite(invite_id)


@workspace_user_invite_namespace.route("/accept_by_token", methods=["PUT"])
class TokenInviteEndpoint(Resource):
    @workspace_user_invite_namespace.expect(
        workspace_user_invite_schema_retriever.retrieve("invite_accept_by_token"),
        validate=True,
    )
    @workspace_user_invite_namespace.doc(
        description="Accepts an invite through token sent from mail."
    )
    @workspace_user_invite_namespace.response(
        HttpStatus.OK.value,
        "Invite accepted successfully",
    )
    @workspace_user_invite_namespace.response(
        HttpStatus.NOT_FOUND.value, "Invite not found or expired."
    )
    @workspace_user_invite_namespace.response(
        HttpStatus.UNAUTHORIZED.value, "Authentication is required"
    )
    @jwt_required()
    def put(self):
        return WorkspaceUserInviteRepository.accept_user_invite_by_token(
            request.get_json()
        )
