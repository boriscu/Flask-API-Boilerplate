from flask import abort
from flask_jwt_extended import jwt_required
from flask_restx import Resource, marshal_with

from app.models.enums.http_status import HttpStatus
from app.services.workspace_services.workspace_repository import WorkspaceRepository
from . import workspace_namespace, workspace_schema_retriever


@workspace_namespace.route("/", methods=["POST"])
class BaseWorkspaceEndpoint(Resource):
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
