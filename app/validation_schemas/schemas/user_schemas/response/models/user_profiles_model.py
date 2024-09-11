from flask_restx import fields
from app.validation_schemas.schemas.user_schemas.response.models.user_profile_model import (
    user_profile_model,
)

user_profiles_model = (
    "UserProfilesModel",
    {
        "users": fields.List(fields.Nested(user_profile_model)),
        "total_entries": fields.Integer(
            description="Total number of users", example=100
        ),
        "total_pages": fields.Integer(description="Total number of pages", example=10),
    },
)
