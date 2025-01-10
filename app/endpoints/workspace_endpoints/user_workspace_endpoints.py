from flask_jwt_extended import jwt_required
from flask_restx import Resource, marshal_with

from app.models.enums.http_status import HttpStatus
from app.services.workspace_services.workspace_crud_service import WorkspaceCRUDService
from . import workspace_namespace, workspace_schema_retriever


@workspace_namespace.route("/current", methods=["GET"])
class CurrentWorkspaceEndpoint(Resource):
    @workspace_namespace.doc(description="Retrieve current user workspace")
    @workspace_namespace.response(
        HttpStatus.OK.value,
        "Workspace retrieved succesfully.",
        workspace_schema_retriever.retrieve("workspace"),
    )
    @workspace_namespace.response(HttpStatus.UNAUTHORIZED.value, "Unauthorized")
    @marshal_with(workspace_schema_retriever.retrieve("workspace"))
    @jwt_required()
    def get(self):
        return WorkspaceCRUDService.get_current_workspace()
