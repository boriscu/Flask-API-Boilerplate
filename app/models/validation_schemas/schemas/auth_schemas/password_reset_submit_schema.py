from flask_restx import fields


def get_password_reset_submit_schema(namespace):
    password_reset_submit_schema = namespace.model(
        "Password reset submit",
        {
            "password": fields.String(
                description="New password for the user",
                example="NewPassword456!",
            ),
            "token": fields.String(
                description="Token for password reset", example="asod123oia900..."
            ),
        },
    )
    return password_reset_submit_schema
