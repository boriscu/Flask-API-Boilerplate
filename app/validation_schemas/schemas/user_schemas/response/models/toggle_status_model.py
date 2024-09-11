from flask_restx import fields

toggle_status_model = (
    "ToggleUserStatusResponse",
    {
        "message": fields.String(
            required=True,
            description="A message indicating the result of the status toggle operation.",
            example="User status changed to active.",
        ),
        "new_status": fields.Boolean(
            required=True,
            description="The new active status of the user after the toggle operation.",
            example=True,
        ),
    },
)
