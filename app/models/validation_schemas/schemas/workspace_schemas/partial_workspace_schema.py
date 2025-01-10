from flask_restx import fields
from datetime import datetime


def get_partial_workspace_schema(namespace):
    partial_workspace_schema = namespace.model(
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
    return partial_workspace_schema
