from flask_restx import fields


def get_admin_change_password_schema(namespace):
    admin_change_password_schema = namespace.model(
        "Admin change password",
        {
            "new_password": fields.String(
                required=True,
                description="New password for the user",
                example="AdminSetPassword789!",
            ),
        },
    )
    return admin_change_password_schema
