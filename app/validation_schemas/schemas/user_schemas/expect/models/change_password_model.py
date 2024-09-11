from flask_restx import fields

change_password_model = (
    "ChangePassword",
    {
        "old_password": fields.String(
            required=True,
            description="Current password of the user",
            example="OldPassword123!",
        ),
        "new_password": fields.String(
            required=True,
            description="New password for the user",
            example="NewPassword456!",
        ),
    },
)
