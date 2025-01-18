from flask_restx import fields


def get_password_reset_request_schema(namespace):
    password_reset_request_schema = namespace.model(
        "Password reset request",
        {
            "email": fields.String(
                description="Email of the user requesting password reset",
                example="john@mail.com",
            ),
        },
    )
    return password_reset_request_schema
