from flask_restx import reqparse
from app.helpers.date_formater import DateFormatter
from werkzeug.datastructures import FileStorage


def get_update_user_schema(namespace):
    update_user_schema = reqparse.RequestParser(bundle_errors=True)
    update_user_schema.add_argument(
        "name",
        type=str,
        required=False,
        location="form",
        help="First name of the user. Example: John",
    )
    update_user_schema.add_argument(
        "surname",
        type=str,
        required=False,
        location="form",
        help="Last name of the user. Example: Doe",
    )
    update_user_schema.add_argument(
        "birthday",
        type=DateFormatter.date_from_string,
        required=False,
        location="form",
        help="User's date of birth. Example: 2001-11-27",
    )
    update_user_schema.add_argument(
        "sex",
        type=str,
        required=False,
        location="form",
        help="Sex of the user. Example: Male",
        choices=["Male", "Female", "Other"],
    )
    update_user_schema.add_argument(
        "profession",
        type=str,
        required=False,
        location="form",
        help="Profession of the user. Example: Student",
        choices=["Student", "Employed", "Teaching", "Retired", "Unemployed"],
    )
    update_user_schema.add_argument(
        "is_sso",
        type=bool,
        required=False,
        location="form",
        help="Is the user using single sign on authentication, only the admin can submit this param. Example: False",
    )
    update_user_schema.add_argument(
        "workspace_creation_quota",
        type=int,
        required=False,
        location="form",
        help="Number of workspaces the user can create. Example: 3",
    )
    update_user_schema.add_argument(
        "profile_picture",
        type=FileStorage,
        location="files",
        required=False,
        help="User profile picture",
    )
    return update_user_schema
