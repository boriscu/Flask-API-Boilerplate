from flask_restx import fields
from datetime import datetime


def get_invitor_schema(namespace):
    partial_user_schema = namespace.model(
        "Invitor",
        {
            "name": fields.String(description="First name of the user", example="John"),
            "surname": fields.String(description="Surname of the user", example="Doe"),
            "email": fields.String(
                description="Email address of the user", example="john.doe@mail.com"
            ),
            "profile_picture": fields.String(
                description="A binary string representing the compressed profile picture.",
                example="Base64 encoded PNG image data",
            ),
            "id": fields.Integer(description="ID of the user profile", example=2),
        },
    )
    return partial_user_schema
