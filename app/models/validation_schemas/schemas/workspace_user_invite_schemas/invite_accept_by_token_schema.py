from flask_restx import fields


def get_user_invite_accept_by_token_schema(namespace):
    user_invite_accept_by_token_schema = namespace.model(
        "User invite accept by token",
        {
            "invite_email": fields.String(
                description="Email address of the invited user",
                example="john.doe@mail.com",
            ),
            "invite_token": fields.String(
                description="Token for user invite accept", example="asod123oia900..."
            ),
        },
    )
    return user_invite_accept_by_token_schema
