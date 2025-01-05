from flask_restx import fields, reqparse
from werkzeug.datastructures import FileStorage


def create_workspace_models(namespace):
    file_upload_parser = reqparse.RequestParser(bundle_errors=True)
    file_upload_parser.add_argument(
        "name",
        type=str,
        required=True,
        location="form",
        help="Name of the workspace",
        default="Development",
    )
    file_upload_parser.add_argument(
        "description",
        type=str,
        location="form",
        help="Description of the workspace",
        default="Workspace for development team",
    )
    file_upload_parser.add_argument(
        "namespaces",
        type=str,
        location="form",
        help="Comma-separated list of namespaces",
        default="[company1.com,company2.co]",
    )
    file_upload_parser.add_argument(
        "icon_image",
        type=FileStorage,
        location="files",
        required=False,
        help="Upload workspace icon image",
    )

    return {"file_upload_parser": file_upload_parser}
