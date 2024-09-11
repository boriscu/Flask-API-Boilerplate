from flask_restx import fields


is_admin_model = (
    "UserIsAdmin",
    {
        "is_admin": fields.Boolean(
            description="Determines if the user is an admin", example=True
        )
    },
)
