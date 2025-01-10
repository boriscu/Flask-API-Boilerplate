from flask_restx import fields


def get_toggle_user_status_response_schema(namespace):
    toggle_user_status_response_schema = namespace.model(
        "Togle user status response",
        {
            "msg": fields.String(
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
    return toggle_user_status_response_schema
