from datetime import datetime
from flask_restx import fields
from flask_restx import reqparse


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
            "id": fields.Integer(description="ID of the user profile", example=2),
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

    change_password_model = namespace.model(
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

    admin_change_password_model = namespace.model(
        "AdminChangePassword",
        {
            "new_password": fields.String(
                required=True,
                description="New password for the user",
                example="AdminSetPassword789!",
            ),
        },
    )

    user_response_model = namespace.model(
        "UserPaginationResponse",
        {
            "users": fields.List(fields.Nested(user_profile_model)),
            "total_entries": fields.Integer(
                description="Total number of users", example=100
            ),
            "total_pages": fields.Integer(
                description="Total number of pages", example=10
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
        "change_password": change_password_model,
        "admin_change_password": admin_change_password_model,
        "users_response": user_response_model,
    }


def create_pagination_parser():
    pagination_parser = reqparse.RequestParser(bundle_errors=True)
    pagination_parser.add_argument(
        "page", type=int, default=1, required=False, help="Page number"
    )
    pagination_parser.add_argument(
        "per_page", type=int, default=10, required=False, help="Items per page"
    )
    pagination_parser.add_argument(
        "sort_field", type=str, default="name", required=False, help="Field to sort by"
    )
    pagination_parser.add_argument(
        "sort_order",
        type=str,
        default="asc",
        required=False,
        help="Sort order: asc or desc",
    )
    pagination_parser.add_argument(
        "search", type=str, required=False, help="Search query"
    )
    pagination_parser.add_argument(
        "filters",
        type=str,
        required=False,
        help="Filtering criteria as a JSON string",
        default='{"is_active":true}',
    )
    return pagination_parser
