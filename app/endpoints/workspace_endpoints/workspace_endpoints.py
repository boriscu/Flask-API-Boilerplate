from flask_jwt_extended import jwt_required
from flask_restx import Resource, marshal_with

from app.models.enums.http_status import HttpStatus

from app.services.workspace_services.workspace_crud_service import WorkspaceCRUDService

from . import workspace_namespace, workspace_schema_retriever


@workspace_namespace.route("/", methods=["GET", "POST"])
class Workspace(Resource):
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
        return WorkspaceCRUDService.create_workspace(
            workspace_schema_retriever.retrieve("create_workspace_request").parse_args()
        )

    @workspace_namespace.doc(
        description="Fetches all workspaces with pagination, sorting, and filtering. Requires admin privileges."
    )
    @jwt_required
    @workspace_namespace.expect(
        workspace_schema_retriever.retrieve("pagination_parser")
    )
    @workspace_namespace.response(
        HttpStatus.OK.value,
        "Workspaces fetched successfully.",
        model=workspace_schema_retriever.retrieve("workspaces"),
    )
    @workspace_namespace.response(HttpStatus.UNAUTHORIZED.value, "Unauthorized.")
    @marshal_with(workspace_schema_retriever.retrieve("workspaces"))
    def get(self):
        args = workspace_schema_retriever.retrieve("pagination_parser").parse_args()

        workspaces, total_entries, total_pages = (
            WorkspaceCRUDService.get_all_workspaces(args)
        )

        return {
            "workspaces": workspaces,
            "total_entries": total_entries,
            "total_pages": total_pages,
        }, HttpStatus.OK.value
