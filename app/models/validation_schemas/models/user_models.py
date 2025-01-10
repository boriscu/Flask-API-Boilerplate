from datetime import datetime
from flask_restx import fields, reqparse
from werkzeug.datastructures import FileStorage

from app.helpers.date_formater import DateFormatter


def create_user_models(namespace):
    user_registration_model = reqparse.RequestParser(bundle_errors=True)
    user_registration_model.add_argument(
        "name",
        type=str,
        required=True,
        location="form",
        help="First name of the user. Example: John",
    )
    user_registration_model.add_argument(
        "surname",
        type=str,
        required=True,
        location="form",
        help="Last name of the user. Example: Doe",
    )
    user_registration_model.add_argument(
        "email",
        type=str,
        required=True,
        location="form",
        help="Email address of the user, must be unique. Example: john@mail.com",
    )
    user_registration_model.add_argument(
        "password",
        type=str,
        required=True,
        location="form",
        help="Password for account creation. Example: Strong password",
    )
    user_registration_model.add_argument(
        "birthday",
        type=DateFormatter.date_from_string,
        required=False,
        location="form",
        help="User's date of birth. Example: 2001-11-27",
    )
    user_registration_model.add_argument(
        "sex",
        type=str,
        required=False,
        location="form",
        help="Sex of the user. Example: Male",
        choices=["Male", "Female", "Other"],
    )
    user_registration_model.add_argument(
        "profession",
        type=str,
        required=False,
        location="form",
        help="Profession of the user. Example: Student",
        choices=["Student", "Employed", "Teaching", "Retired", "Unemployed"],
    )
    user_registration_model.add_argument(
        "is_sso",
        type=bool,
        required=False,
        location="form",
        help="Is the user using single sign on authentication, only the admin can submit this param. Example: False",
        default=False,
    )
    user_registration_model.add_argument(
        "is_active",
        type=bool,
        required=False,
        location="form",
        help="Should the user account be active, only the admin can submit this param. Example: False",
        default=False,
    )
    user_registration_model.add_argument(
        "profile_picture",
        type=FileStorage,
        location="files",
        required=False,
        help="User profile picture",
    )

    user_login_request_model = namespace.model(
        "User login request",
        {
            "email": fields.String(
                required=True,
                description="User email address",
                example="admin@mail.com",
            ),
            "password": fields.String(
                required=True, description="User password", example="admin"
            ),
        },
    )

    user_login_response_model = namespace.model(
        "User login response",
        {
            "msg": fields.String(
                required=True,
                description="Response message",
                example="Login successful",
            ),
            "access_token": fields.String(
                required=True,
                description="JWT Token for the user that needs to be used for authentication",
                example="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c",
            ),
        },
    )

    full_user_profile_model = namespace.model(
        "Full User",
        {
            "name": fields.String(description="First name of the user", example="John"),
            "surname": fields.String(description="Surname of the user", example="Doe"),
            "email": fields.String(
                description="Email address of the user", example="john.doe@mail.com"
            ),
            "birthday": fields.Date(
                description="User's date of birth", example="1990-01-01"
            ),
            "sex": fields.String(
                description="Sex of the user",
                enum=["Male", "Female", "Other"],
                example="Male",
            ),
            "profession": fields.String(
                description="Profession of the user",
                enum=["Student", "Employed", "Teaching", "Retired", "Unemployed"],
                example="Employed",
            ),
            "is_admin": fields.Boolean(
                description="Flag noting if the user has the admin role",
                example=False,
            ),
            "is_active": fields.Boolean(
                description="Flag noting if the user is active or not", example=True
            ),
            "is_sso": fields.Boolean(
                description="Flag noting if the user is using single sign on authentication",
                example=False,
            ),
            "profile_picture": fields.String(
                description="A binary string representing the compressed profile picture.",
                example="Base64 encoded PNG image data",
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

    partial_user_model = namespace.model(
        "Partial User",
        {
            "name": fields.String(description="First name of the user", example="John"),
            "surname": fields.String(description="Surname of the user", example="Doe"),
            "email": fields.String(
                description="Email address of the user", example="john.doe@mail.com"
            ),
            "birthday": fields.Date(
                description="User's date of birth", example="1990-01-01"
            ),
            "sex": fields.String(
                description="Sex of the user",
                enum=["Male", "Female", "Other"],
                example="Male",
            ),
            "profession": fields.String(
                description="Profession of the user",
                enum=["Student", "Employed", "Teaching", "Retired", "Unemployed"],
                example="Employed",
            ),
            "is_admin": fields.Boolean(
                description="Flag noting if the user has the admin role",
                example=False,
            ),
            "is_active": fields.Boolean(
                description="Flag noting if the user is active or not", example=True
            ),
            "is_sso": fields.Boolean(
                description="Flag noting if the user is using single sign on authentication",
                example=False,
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

    toggle_user_status_response_model = namespace.model(
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

    change_password_model = namespace.model(
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

    admin_change_password_model = namespace.model(
        "Admin change password",
        {
            "new_password": fields.String(
                required=True,
                description="New password for the user",
                example="AdminSetPassword789!",
            ),
        },
    )

    all_users_model = namespace.model(
        "Users",
        {
            "users": fields.List(fields.Nested(partial_user_model)),
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
        "login_request": user_login_request_model,
        "login_response": user_login_response_model,
        "profile": full_user_profile_model,
        "toggle_status": toggle_user_status_response_model,
        "change_password": change_password_model,
        "admin_change_password": admin_change_password_model,
        "users_response": all_users_model,
    }
