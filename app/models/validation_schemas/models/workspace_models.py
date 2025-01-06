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

    return {
        "create_workspace_request": create_workspace_request,
        "create_workspace_response": create_workspace_response,
    }
