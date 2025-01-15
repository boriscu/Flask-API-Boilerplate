from flask_restx import fields
from datetime import datetime

from app.models.validation_schemas.schemas.workspace_schemas.partial_workspace_schema import (
    get_partial_workspace_schema,
)
from app.models.validation_schemas.schemas.workspace_user_invite_schemas.invitor_schema import (
    get_invitor_schema,
)


def get_invite_schema(namespace):
    full_workspace_schema = namespace.model(
        "Invite",
        {
            "workspace_user_role": fields.Integer(
                description="Role that the user will receive at the workspace. View = 0, Edit = 1",
                example=1,
            ),
            "created_at": fields.DateTime(
                dt_format="iso8601",
                description="The date and time when the invite was initially created.",
                example=datetime.now().isoformat(),
            ),
            "id": fields.Integer(
                description="A unique identifier for the invite.", example=101
            ),
            "workspace": fields.Nested(get_partial_workspace_schema(namespace)),
            "invitor": fields.Nested(get_invitor_schema(namespace)),
        },
    )
    return full_workspace_schema
