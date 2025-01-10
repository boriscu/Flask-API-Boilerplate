from flask_restx import fields
from datetime import datetime


def get_partial_user_schema(namespace):
    partial_user_schema = namespace.model(
        "Partial User",
        {
            "name": fields.String(description="First name of the user", example="John"),
            "surname": fields.String(description="Surname of the user", example="Doe"),
            "email": fields.String(
                description="Email address of the user", example="john.doe@mail.com"
            ),
            "birthday": fields.Date(
                description="User's date of birth", example="1990-01-01"
            ),
            "sex": fields.String(
                description="Sex of the user",
                enum=["Male", "Female", "Other"],
                example="Male",
            ),
            "profession": fields.String(
                description="Profession of the user",
                enum=["Student", "Employed", "Teaching", "Retired", "Unemployed"],
                example="Employed",
            ),
            "is_admin": fields.Boolean(
                description="Flag noting if the user has the admin role",
                example=False,
            ),
            "is_active": fields.Boolean(
                description="Flag noting if the user is active or not", example=True
            ),
            "is_sso": fields.Boolean(
                description="Flag noting if the user is using single sign on authentication",
                example=False,
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
    return partial_user_schema
