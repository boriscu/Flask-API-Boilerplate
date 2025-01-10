from flask_restx import reqparse
from werkzeug.datastructures import FileStorage


def get_workspace_creation_schema():
    workspace_creation_schema = reqparse.RequestParser(bundle_errors=True)
    workspace_creation_schema.add_argument(
        "name",
        type=str,
        required=True,
        location="form",
        help="Name of the workspace",
    )
    workspace_creation_schema.add_argument(
        "description",
        type=str,
        location="form",
        help="Description of the workspace",
    )
    workspace_creation_schema.add_argument(
        "namespaces",
        type=str,
        location="form",
        help="Comma-separated list of namespaces",
    )
    workspace_creation_schema.add_argument(
        "icon_image",
        type=FileStorage,
        location="files",
        required=False,
        help="Upload workspace icon image",
    )
    return workspace_creation_schema
