from flask import request
from flask_jwt_extended import jwt_required
from flask_restx import Resource, marshal_with

from app.models.enums.http_status import HttpStatus

from app.helpers.http_response_generator import HttpResponseGenerator

from app.services.user_services.user_auth_service import UserAuthService
from app.services.user_services.user_repository import UserRepository

from . import user_namespace, user_schema_retriever


@user_namespace.route("/", methods=["GET"])
class BaseUserEndpoint(Resource):
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
    @marshal_with(user_schema_retriever.retrieve("users_response"))
    @jwt_required()
    def get(self):
        args = user_schema_retriever.retrieve("pagination_parser").parse_args()

        users, total_entries, total_pages = UserRepository.get_all_users(args)

        return {
            "users": users,
            "total_entries": total_entries,
            "total_pages": total_pages,
        }, HttpStatus.OK.value


@user_namespace.route("/<int:user_id>", methods=["GET", "DELETE", "PUT"])
class SingleUserEndpoint(Resource):
    @user_namespace.doc(
        description="Retrieve any user's profile by user ID. Requires admin privileges."
    )
    @user_namespace.response(
        HttpStatus.OK.value,
        "User profile retrieved successfully.",
        user_schema_retriever.retrieve("profile"),
    )
    @user_namespace.response(HttpStatus.NOT_FOUND.value, "User not found")
    @user_namespace.response(HttpStatus.UNAUTHORIZED.value, "Unauthorized")
    @marshal_with(user_schema_retriever.retrieve("profile"))
    @jwt_required()
    def get(self, user_id):
        return UserRepository.get_single_user(user_id=user_id, check_admin=True)

    @user_namespace.doc(
        description="Delete a user based on the user ID.  Requires admin privileges."
    )
    @user_namespace.response(HttpStatus.OK.value, "User deleted succesfully")
    @user_namespace.response(HttpStatus.FORBIDDEN.value, "Can't delete an admin user")
    @user_namespace.response(HttpStatus.UNAUTHORIZED.value, "Unauthorized")
    @jwt_required()
    def delete(self, user_id):
        return UserRepository.delete_user(user_id)

    @user_namespace.doc(
        description="Update a user. Admin can update any user. Only the admin can change the is_sso field"
    )
    @user_namespace.expect(user_schema_retriever.retrieve("update_user"), validate=True)
    @user_namespace.response(HttpStatus.OK.value, "User updated succesfully")
    @user_namespace.response(HttpStatus.UNAUTHORIZED.value, "Unauthorized")
    @user_namespace.response(HttpStatus.BAD_REQUEST.value, "Bad request")
    def put(self, user_id):
        return UserRepository.update_user(
            user_id, user_schema_retriever.retrieve("update_user").parse_args()
        )


@user_namespace.route("/<int:user_id>/status/", methods=["PUT"])
class UserStatusEndpoint(Resource):
    @user_namespace.doc(
        description="Toggle user's active status by user ID. Requires admin privileges."
    )
    @user_namespace.response(
        HttpStatus.OK.value,
        "User status updated successfully.",
        user_schema_retriever.retrieve("toggle_status"),
    )
    @user_namespace.response(HttpStatus.NOT_FOUND.value, "User not found")
    @user_namespace.response(HttpStatus.UNAUTHORIZED.value, "Unauthorized")
    @jwt_required()
    def put(self, user_id):
        user_profile = UserRepository.get_single_user(user_id, check_admin=True)
        new_status, message = UserRepository.toggle_active_status(user_profile)

        return {"msg": message, "is_active": new_status}, HttpStatus.OK.value


@user_namespace.route("/change-password/<int:user_id>", methods=["PUT"])
class AdminPasswordEndpoint(Resource):
    @user_namespace.doc(
        description="Allows admin to change the password for a specified user by user ID. Requires admin privileges."
    )
    @user_namespace.expect(
        user_schema_retriever.retrieve("admin_change_password"), validate=True
    )
    @user_namespace.response(HttpStatus.OK.value, "Password changed successfully.")
    @user_namespace.response(HttpStatus.UNAUTHORIZED.value, "Unauthorized.")
    @jwt_required()
    def put(self, user_id):
        data = request.json

        user = UserRepository.get_single_user(user_id, check_admin=True)

        UserAuthService.change_password(user, data.get("new_password"))

        return HttpResponseGenerator.generate_response(HttpStatus.OK)
