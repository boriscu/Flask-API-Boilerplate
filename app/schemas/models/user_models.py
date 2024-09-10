from datetime import datetime
from flask_restx import fields


def create_user_models(namespace):
    user_registration_model = namespace.model(
        "UserRegistration",
        {
            "name": fields.String(
                required=True, description="First name of the user", example="John"
            ),
            "surname": fields.String(
                required=True, description="Surname of the user", example="Doe"
            ),
            "email": fields.String(
                required=True,
                description="Email address of the user, must be unique",
                example="john.doe@mail.com",
            ),
            "password": fields.String(
                required=True,
                description="Password for account creation",
                example="Strong password",
            ),
        },
    )

    user_login_model = namespace.model(
        "UserLogin",
        {
            "email": fields.String(
                required=True,
                description="User email address",
                example="john.doe@mail.com",
            ),
            "password": fields.String(
                required=True, description="User password", example="Strong password"
            ),
        },
    )

    user_profile_model = namespace.model(
        "UserProfile",
        {
            "name": fields.String(description="First name of the user", example="John"),
            "surname": fields.String(description="Surname of the user", example="Doe"),
            "email": fields.String(
                description="Email address of the user", example="john.doe@mail.com"
            ),
            "is_admin": fields.Boolean(
                description="Flag noting if the user has the admin role",
                example=False,
            ),
            "is_active": fields.Boolean(
                description="Flag noting if the user is active or not", example=True
            ),
            "created_at": fields.DateTime(
                dt_format="iso8601",
                description="Date the user was created",
                example=datetime.now().isoformat(),
            ),
            "updated_at": fields.DateTime(
                dt_format="iso8601",
                description="Date the user profile was last updated",
                example=datetime.now().isoformat(),
            ),
        },
    )

    user_is_admin_model = namespace.model(
        "UserIsAdmin",
        {
            "is_admin": fields.Boolean(
                description="Determines if the user is an admin", example=True
            )
        },
    )

    user_is_active_model = namespace.model(
        "UserIsActive",
        {
            "is_active": fields.Boolean(
                description="Determines if the user is active", example=True
            )
        },
    )

    toggle_user_status_response_model = namespace.model(
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

    return {
        "registration": user_registration_model,
        "login": user_login_model,
        "profile": user_profile_model,
        "is_admin": user_is_admin_model,
        "is_active": user_is_active_model,
        "toggle_status": toggle_user_status_response_model,
    }
