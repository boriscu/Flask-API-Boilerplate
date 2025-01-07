from flask import abort, json, request
from flask_jwt_extended import get_jwt, get_jwt_identity, jwt_required
from flask_restx import Resource, marshal_with

from app.models.enums.http_status import HttpStatus

from app.helpers.http_response_generator import HttpResponseGenerator

from app.services.user_services.user_auth_service import UserAuthService
from app.services.user_services.user_crud_service import UserCRUDService
from app.services.user_services.user_pagination_service import UserPaginationService

from . import user_namespace, user_schema_retriever


@user_namespace.route("/<int:user_id>")
class GetUserById(Resource):
    @user_namespace.doc(
        description="Retrieve any user's profile by user ID. Requires admin privileges."
    )
    @jwt_required()
    @user_namespace.response(
        HttpStatus.OK.value,
        "User profile retrieved successfully.",
        user_schema_retriever.retrieve("profile"),
    )
    @user_namespace.response(HttpStatus.NOT_FOUND.value, "User not found")
    @user_namespace.response(HttpStatus.UNAUTHORIZED.value, "Unauthorized")
    @user_namespace.response(HttpStatus.INTERNAL_SERVER_ERROR.value, "Server error")
    @marshal_with(user_schema_retriever.retrieve("profile"))
    def get(self, user_id):
        return UserCRUDService.get_single_user(user_id)


@user_namespace.route("/<int:user_id>/status/")
class ToggleUserStatus(Resource):
    @user_namespace.doc(
        description="Toggle user's active status by user ID. Requires admin privileges."
    )
    @jwt_required()
    @user_namespace.response(
        HttpStatus.OK.value,
        "User status updated successfully.",
        user_schema_retriever.retrieve("toggle_status"),
    )
    @user_namespace.response(HttpStatus.NOT_FOUND.value, "User not found")
    @user_namespace.response(HttpStatus.UNAUTHORIZED.value, "Unauthorized")
    @user_namespace.response(HttpStatus.INTERNAL_SERVER_ERROR.value, "Server error")
    def put(self, user_id):
        user_profile = UserCRUDService.get_single_user(user_id)
        new_status, message = UserCRUDService.toggle_active_status(user_profile)

        return {"msg": message, "is_active": new_status}, HttpStatus.OK.value


@user_namespace.route("/change-password/<int:user_id>")
class AdminChangePassword(Resource):
    @user_namespace.doc(
        description="Allows admin to change the password for a specified user by user ID. Requires admin privileges."
    )
    @user_namespace.expect(
        user_schema_retriever.retrieve("admin_change_password"), validate=True
    )
    @jwt_required()
    @user_namespace.response(HttpStatus.OK.value, "Password changed successfully.")
    @user_namespace.response(HttpStatus.NOT_FOUND.value, "User not found.")
    @user_namespace.response(HttpStatus.UNAUTHORIZED.value, "Unauthorized.")
    @user_namespace.response(HttpStatus.INTERNAL_SERVER_ERROR.value, "Server error.")
    @user_namespace.response(HttpStatus.BAD_REQUEST.value, "Bad request")
    def put(self, user_id):
        data = request.json

        user = UserCRUDService.get_single_user(user_id)

        UserAuthService.change_password(user, data.get("new_password"))

        return HttpResponseGenerator.generate_response(HttpStatus.OK.value)


@user_namespace.route("/")
class GetUsers(Resource):
    @user_namespace.doc(
        description="Fetches all users with pagination, sorting, and filtering. Requires admin privileges."
    )
    @user_namespace.expect(
        user_schema_retriever.retrieve("pagination_parser"), validate=True
    )
    @user_namespace.response(
        HttpStatus.OK.value,
        "Users fetched successfully.",
        model=user_schema_retriever.retrieve("users_response"),
    )
    @user_namespace.response(HttpStatus.UNAUTHORIZED.value, "Unauthorized.")
    @user_namespace.response(HttpStatus.INTERNAL_SERVER_ERROR.value, "Server error.")
    @marshal_with(user_schema_retriever.retrieve("users_response"))
    @jwt_required()
    def get(self):
        args = user_schema_retriever.retrieve("pagination_parser").parse_args()

        users, total_entries, total_pages = UserCRUDService.get_all_users(args)

        return {
            "users": users,
            "total_entries": total_entries,
            "total_pages": total_pages,
        }, HttpStatus.OK.value
