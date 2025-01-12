from flask_restx import fields
from datetime import datetime


def get_full_workspace_schema(namespace):
    full_workspace_schema = namespace.model(
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
            "user_role": fields.Integer(
                description="An integer representing the users role in the workspace. View = 0, Edit = 1, Admin = 2",
                example=2,
            ),
            "is_personal": fields.Boolean(
                description="A flag representing if the workspace is personal. Each user has only 1 personal workspace",
                example=False,
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
    return full_workspace_schema
