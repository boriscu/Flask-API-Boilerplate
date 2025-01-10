from flask_restx import fields


def get_login_request_schema(namespace):
    user_login_request_schema = namespace.model(
        "User login request",
        {
            "email": fields.String(
                required=True,
                description="User email address",
                example="admin@mail.com",
            ),
            "password": fields.String(
                required=True, description="User password", example="admin"
            ),
        },
    )
    return user_login_request_schema
