from flask_restx import fields

is_active_model = (
    "UserIsActive",
    {
        "is_active": fields.Boolean(
            description="Determines if the user is active", example=True
        )
    },
)
