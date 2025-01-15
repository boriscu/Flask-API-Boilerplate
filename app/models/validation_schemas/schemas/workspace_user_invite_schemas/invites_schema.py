from flask_restx import fields

from app.models.validation_schemas.schemas.workspace_user_invite_schemas.invite_schema import (
    get_invite_schema,
)


def get_all_invites_schema(namespace):
    all_invites_schema = namespace.model(
        "Invites",
        {
            "invites": fields.List(fields.Nested(get_invite_schema(namespace))),
            "total_entries": fields.Integer(
                description="Total number of invites", example=10
            ),
            "total_pages": fields.Integer(
                description="Total number of pages", example=2
            ),
        },
    )
    return all_invites_schema
