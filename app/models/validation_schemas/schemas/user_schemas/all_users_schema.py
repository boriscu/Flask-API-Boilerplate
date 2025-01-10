from flask_restx import fields

from app.models.validation_schemas.schemas.user_schemas.partial_user_schema import (
    get_partial_user_schema,
)


def get_all_users_schema(namespace):
    all_users_model = namespace.model(
        "Users",
        {
            "users": fields.List(fields.Nested(get_partial_user_schema(namespace))),
            "total_entries": fields.Integer(
                description="Total number of users", example=100
            ),
            "total_pages": fields.Integer(
                description="Total number of pages", example=10
            ),
        },
    )
    return all_users_model
