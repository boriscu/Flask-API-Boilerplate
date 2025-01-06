from flask import Response, abort
from flask_jwt_extended import jwt_required
from flask_restx import Resource

from app.helpers.http_response_generator import HttpResponseGenerator
from app.models.enums.http_status import HttpStatus

from app.services.workspace_services.workspace_crud_service import WorkspaceCRUDService

from . import workspace_namespace, workspace_schema_retriever


@workspace_namespace.route("/", methods=["POST"])
class CreateWorkspace(Resource):
    @workspace_namespace.doc(
        description="Creates a workspace. Requires admin privileges."
    )
    @jwt_required()
    @workspace_namespace.expect(
        workspace_schema_retriever.retrieve("create_workspace_request")
    )
    @workspace_namespace.response(
        HttpStatus.CREATED.value,
        "Workspace created successfully",
        workspace_namespace.model(
            "WorkspaceCreationResponse",
            workspace_schema_retriever.retrieve("create_workspace_response"),
        ),
    )
    @workspace_namespace.response(
        HttpStatus.BAD_REQUEST.value, "Invalid input or missing required fields"
    )
    @workspace_namespace.response(
        HttpStatus.UNAUTHORIZED.value, "Authentication is required"
    )
    def post(self):
        try:
            args = workspace_schema_retriever.retrieve(
                "create_workspace_request"
            ).parse_args()
            return WorkspaceCRUDService.create_workspace(args)
        except Exception as e:
            print(e)
            return HttpResponseGenerator.generate_response(
                HttpStatus.INTERNAL_SERVER_ERROR.value
            )
