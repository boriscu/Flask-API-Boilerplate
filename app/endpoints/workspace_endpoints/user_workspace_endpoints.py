from flask import abort
from flask_jwt_extended import jwt_required
from flask_restx import Resource, marshal_with

from app.models.enums.http_status import HttpStatus
from app.services.workspace_services.workspace_repository import WorkspaceRepository
from . import workspace_namespace, workspace_schema_retriever


@workspace_namespace.route("/", methods=["POST", "GET"])
class BaseUserWorkspaceEndpoint(Resource):
    @workspace_namespace.doc(description="Creates a workspace.")
    @workspace_namespace.expect(
        workspace_schema_retriever.retrieve("create_workspace_request")
    )
    @workspace_namespace.response(
        HttpStatus.CREATED.value,
        "Workspace created successfully",
        model=workspace_schema_retriever.retrieve("create_workspace_response"),
    )
    @workspace_namespace.response(
        HttpStatus.UNAUTHORIZED.value, "Authentication is required"
    )
    @workspace_namespace.response(
        HttpStatus.NOT_ACCEPTABLE.value, "User is over their workspace creation quota"
    )
    @jwt_required()
    def post(self):
        return WorkspaceRepository.create_workspace(
            workspace_schema_retriever.retrieve("create_workspace_request").parse_args()
        )

    @workspace_namespace.doc(
        description="Fetches accessible workspaces with pagination, sorting, and filtering. Administrator can retrieve all existing workspaces."
    )
    @workspace_namespace.expect(
        workspace_schema_retriever.retrieve("pagination_parser"), validate=True
    )
    @workspace_namespace.response(
        HttpStatus.OK.value,
        "Workspaces fetched successfully.",
        model=workspace_schema_retriever.retrieve("workspaces"),
    )
    @workspace_namespace.response(HttpStatus.UNAUTHORIZED.value, "Unauthorized.")
    @marshal_with(workspace_schema_retriever.retrieve("workspaces"))
    @jwt_required()
    def get(self):
        args = workspace_schema_retriever.retrieve("pagination_parser").parse_args()
        workspaces, total_entries, total_pages = WorkspaceRepository.get_all_workspaces(
            args
        )
        return {
            "workspaces": workspaces,
            "total_entries": total_entries,
            "total_pages": total_pages,
        }, HttpStatus.OK.value
