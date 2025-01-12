from flask_restx import fields

from app.models.validation_schemas.schemas.workspace_schemas.full_workspace_schema import (
    get_full_workspace_schema,
)


def get_all_workspace_schema(namespace):
    all_workspaces_schema = namespace.model(
        "Workspaces",
        {
            "workspaces": fields.List(
                fields.Nested(get_full_workspace_schema(namespace))
            ),
            "total_entries": fields.Integer(
                description="Total number of workspaces", example=10
            ),
            "total_pages": fields.Integer(
                description="Total number of pages", example=2
            ),
        },
    )
    return all_workspaces_schema
