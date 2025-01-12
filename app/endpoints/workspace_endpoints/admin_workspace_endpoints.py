from flask import abort
from flask_jwt_extended import jwt_required
from flask_restx import Resource, marshal_with

from app.models.enums.http_status import HttpStatus

from app.services.workspace_services.workspace_repository import WorkspaceRepository

from . import workspace_namespace, workspace_schema_retriever


@workspace_namespace.route("/<int:workspace_id>", methods=["GET", "DELETE", "PUT"])
class SingleWorkspaceEndpoint(Resource):
    @workspace_namespace.doc(
        description="Retrieve any workspace that belongs by workspace ID.  Requires admin privileges."
    )
    @workspace_namespace.response(
        HttpStatus.OK.value,
        "Workspace retrieved succesfully.",
        workspace_schema_retriever.retrieve("workspace"),
    )
    @workspace_namespace.response(HttpStatus.NOT_FOUND.value, "Workspace not found")
    @workspace_namespace.response(HttpStatus.UNAUTHORIZED.value, "Unauthorized")
    @marshal_with(workspace_schema_retriever.retrieve("workspace"))
    @jwt_required()
    def get(self, workspace_id):
        return WorkspaceRepository.get_single_workspace(workspace_id)

    @workspace_namespace.doc(
        description="Delete a workspace based on the workspace ID.  Requires admin privileges."
    )
    @workspace_namespace.response(HttpStatus.OK.value, "Workspace deleted succesfully")
    @workspace_namespace.response(HttpStatus.NOT_FOUND.value, "Workspace not found")
    @workspace_namespace.response(HttpStatus.UNAUTHORIZED.value, "Unauthorized")
    @jwt_required()
    def delete(self, workspace_id):
        return WorkspaceRepository.delete_workspace(workspace_id)

    @workspace_namespace.doc(
        description="Updates a workspace. Requires admin privileges."
    )
    @workspace_namespace.expect(
        workspace_schema_retriever.retrieve("create_workspace_request")
    )
    @workspace_namespace.response(
        HttpStatus.CREATED.value,
        "Workspace updated successfully",
        model=workspace_schema_retriever.retrieve("create_workspace_response"),
    )
    @workspace_namespace.response(
        HttpStatus.UNAUTHORIZED.value, "Authentication is required"
    )
    @jwt_required()
    def put(self, workspace_id):
        return WorkspaceRepository.update_workspace(
            workspace_id,
            workspace_schema_retriever.retrieve(
                "create_workspace_request"
            ).parse_args(),
        )
