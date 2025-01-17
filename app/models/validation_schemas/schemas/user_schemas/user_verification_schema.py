from flask_restx import fields


def get_user_verification_schema(namespace):
    user_verification_schema = namespace.model(
        "User verification",
        {
            "email": fields.String(
                description="User email address", example="user@mail.com"
            ),
            "token": fields.String(
                description="Token for user verification", example="asod123oia900..."
            ),
        },
    )
    return user_verification_schema
