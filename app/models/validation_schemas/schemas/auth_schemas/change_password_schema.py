from flask_restx import fields


def get_change_password_schema(namespace):
    change_password_schema = namespace.model(
        "User change password",
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
    return change_password_schema
