from datetime import datetime
from flask_restx import fields, reqparse
from werkzeug.datastructures import FileStorage


def create_workspace_models(namespace):
    create_workspace_request = reqparse.RequestParser(bundle_errors=True)
    create_workspace_request.add_argument(
        "name",
        type=str,
        required=True,
        location="form",
        help="Name of the workspace",
        default="Development",
    )
    create_workspace_request.add_argument(
        "description",
        type=str,
        location="form",
        help="Description of the workspace",
        default="Workspace for development team",
    )
    create_workspace_request.add_argument(
        "namespaces",
        type=str,
        location="form",
        help="Comma-separated list of namespaces",
        default="[company1.com,company2.com]",
    )
    create_workspace_request.add_argument(
        "icon_image",
        type=FileStorage,
        location="files",
        required=False,
        help="Upload workspace icon image",
    )

    create_workspace_response = namespace.model(
        "WorkspaceCreationResponse",
        {
            "msg": fields.String(
                required=True,
                description="Response message indicating the outcome of the operation",
                example="Workspace created successfully.",
            ),
            "workspace_id": fields.Integer(
                required=True,
                description="The unique identifier of the newly created workspace",
                example=123,
            ),
        },
    )

    full_workspace_model = namespace.model(
        "Full workspace",
        {
            "name": fields.String(
                description="The name of the workspace.", example="University Workspace"
            ),
            "description": fields.String(
                description="A brief summary of what the workspace is used for.",
                example="A dedicated workspace for the University of Novi Sad's research teams.",
            ),
            "namespaces": fields.String(
                description="A list of email domains that are allowed access to the workspace.",
                example="['uns.ac.rs', 'jjzmaj@edu.rs']",
            ),
            "icon_image": fields.String(
                description="A binary string representing the compressed icon image for the workspace.",
                example="Base64 encoded PNG image data",
            ),
            "created_at": fields.DateTime(
                dt_format="iso8601",
                description="The date and time when the workspace was initially created.",
                example=datetime.now().isoformat(),
            ),
            "updated_at": fields.DateTime(
                dt_format="iso8601",
                description="The timestamp of the last update made to the workspace.",
                example=datetime.now().isoformat(),
            ),
            "id": fields.Integer(
                description="A unique identifier for the workspace.", example=101
            ),
        },
    )

    partial_workspace_model = namespace.model(
        "Partial workspace",
        {
            "name": fields.String(
                description="The name of the workspace.", example="University Workspace"
            ),
            "namespaces": fields.String(
                description="A list of email domains that are allowed access to the workspace.",
                example="['uns.ac.rs', 'jjzmaj@edu.rs']",
            ),
            "created_at": fields.DateTime(
                dt_format="iso8601",
                description="The date and time when the workspace was initially created.",
                example=datetime.now().isoformat(),
            ),
            "updated_at": fields.DateTime(
                dt_format="iso8601",
                description="The timestamp of the last update made to the workspace.",
                example=datetime.now().isoformat(),
            ),
            "id": fields.Integer(
                description="A unique identifier for the workspace.", example=101
            ),
        },
    )

    all_workspaces_model = namespace.model(
        "Workspaces",
        {
            "workspaces": fields.List(fields.Nested(partial_workspace_model)),
            "total_entries": fields.Integer(
                description="Total number of workspaces", example=100
            ),
            "total_pages": fields.Integer(
                description="Total number of pages", example=10
            ),
        },
    )
    return {
        "create_workspace_request": create_workspace_request,
        "create_workspace_response": create_workspace_response,
        "workspaces": all_workspaces_model,
        "workspace": full_workspace_model,
    }
