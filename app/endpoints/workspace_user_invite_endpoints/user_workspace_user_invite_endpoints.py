from flask import request
from flask_jwt_extended import jwt_required
from flask_restx import Resource, marshal_with
from app.helpers.http_response_generator import HttpResponseGenerator
from app.models.enums.http_status import HttpStatus
from app.models.pg.workspace_user_invite import WorkspaceUserInvite
from app.services.workspace_user_invite_services.workspace_user_invite_repository import (
    WorkspaceUserInviteRepository,
)

from . import workspace_user_invite_namespace, workspace_user_invite_schema_retriever


@workspace_user_invite_namespace.route("workspace/<int:workspace_id>", methods=["POST"])
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


@workspace_user_invite_namespace.route("/", methods=["GET"])
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


@workspace_user_invite_namespace.route("/<int:invite_id>", methods=["DELETE"])
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
        WorkspaceUserInvite.delete_by_id(invite_id)
        return HttpResponseGenerator
