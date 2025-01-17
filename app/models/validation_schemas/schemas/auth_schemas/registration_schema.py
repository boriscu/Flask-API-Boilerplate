from flask_restx import reqparse
from werkzeug.datastructures import FileStorage


def get_user_registration_schema():
    user_registration_schema = reqparse.RequestParser(bundle_errors=True)
    user_registration_schema.add_argument(
        "name",
        type=str,
        required=True,
        location="form",
        help="First name of the user. Example: John",
    )
    user_registration_schema.add_argument(
        "surname",
        type=str,
        required=True,
        location="form",
        help="Last name of the user. Example: Doe",
    )
    user_registration_schema.add_argument(
        "email",
        type=str,
        required=True,
        location="form",
        help="Email address of the user, must be unique. Example: john@mail.com",
    )
    user_registration_schema.add_argument(
        "password",
        type=str,
        required=True,
        location="form",
        help="Password for account creation. Example: 'Strong password'.",
    )
    user_registration_schema.add_argument(
        "birthday",
        type=str,
        required=False,
        location="form",
        help="User's date of birth. Example: 2001-11-27",
    )
    user_registration_schema.add_argument(
        "sex",
        type=str,
        required=False,
        location="form",
        help="Sex of the user. Example: Male",
        choices=["Male", "Female", "Other"],
    )
    user_registration_schema.add_argument(
        "profession",
        type=str,
        required=False,
        location="form",
        help="Profession of the user. Example: Student",
        choices=["Student", "Employed", "Teaching", "Retired", "Unemployed"],
    )
    user_registration_schema.add_argument(
        "is_sso",
        type=bool,
        required=False,
        location="form",
        help="Is the user using single sign on authentication, only the admin can submit this param. Example: False",
        default=False,
    )
    user_registration_schema.add_argument(
        "is_active",
        type=bool,
        required=False,
        location="form",
        help="Should the user account be active, only the admin can submit this param. Example: False",
        default=False,
    )
    user_registration_schema.add_argument(
        "profile_picture",
        type=FileStorage,
        location="files",
        required=False,
        help="User profile picture",
    )
    return user_registration_schema
