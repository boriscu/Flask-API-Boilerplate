from datetime import datetime
from flask_restx import fields


user_profile_model = (
    "UserProfile",
    {
        "name": fields.String(description="First name of the user", example="John"),
        "surname": fields.String(description="Surname of the user", example="Doe"),
        "email": fields.String(
            description="Email address of the user", example="john.doe@mail.com"
        ),
        "is_admin": fields.Boolean(
            description="Flag noting if the user has the admin role",
            example=False,
        ),
        "is_active": fields.Boolean(
            description="Flag noting if the user is active or not", example=True
        ),
        "created_at": fields.DateTime(
            dt_format="iso8601",
            description="Date the user was created",
            example=datetime.now().isoformat(),
        ),
        "updated_at": fields.DateTime(
            dt_format="iso8601",
            description="Date the user profile was last updated",
            example=datetime.now().isoformat(),
        ),
        "id": fields.Integer(description="ID of the user profile", example=2),
    },
)
