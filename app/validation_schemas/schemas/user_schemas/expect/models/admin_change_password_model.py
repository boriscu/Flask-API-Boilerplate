from flask_restx import fields

admin_change_password_model = (
    "AdminChangePassword",
    {
        "new_password": fields.String(
            required=True,
            description="New password for the user",
            example="AdminSetPassword789!",
        ),
    },
)
