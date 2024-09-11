from flask import json, request
from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_restx import Resource, marshal_with

from peewee import DoesNotExist

from werkzeug.exceptions import Unauthorized

from app.enums.http_status import HttpStatus
from app.logger_setup import LoggerSetup
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
        try:
            current_user_id = get_jwt_identity()
            current_user_profile = UserCRUDService.get_user(current_user_id)

            if not UserAuthService.check_if_admin(current_user_profile):
                return (
                    {"message": "Unauthorized. Only admins can access this endpoint."},
                    HttpStatus.UNAUTHORIZED.value,
                )

            user_profile = UserCRUDService.get_user(user_id)
            if user_profile is None:
                return (
                    {"message": "User not found"},
                    HttpStatus.NOT_FOUND.value,
                )
            return user_profile

        except DoesNotExist:
            return (
                {"message": "User not found"},
                HttpStatus.NOT_FOUND.value,
            )
        except Unauthorized as e:
            return (
                {"message": str(e)},
                HttpStatus.UNAUTHORIZED.value,
            )
        except Exception as e:
            LoggerSetup.get_logger("general").error(
                f"Internal server error while getting the user with ID:{user_id}, err : {e}"
            )
            return (
                {"message": f"Internal server error: {str(e)}"},
                HttpStatus.INTERNAL_SERVER_ERROR.value,
            )


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
        try:
            current_user_id = get_jwt_identity()
            current_user_profile = UserCRUDService.get_user(current_user_id)

            if not UserAuthService.check_if_admin(current_user_profile):
                return (
                    {"message": "Unauthorized."},
                    HttpStatus.UNAUTHORIZED.value,
                )

            user_profile = UserCRUDService.get_user(user_id)

            new_status, message = UserCRUDService.toggle_active_status(user_profile)

            return {"message": message, "is_active": new_status}, HttpStatus.OK.value

        except DoesNotExist:
            return (
                {"message": "User not found"},
                HttpStatus.NOT_FOUND.value,
            )
        except Unauthorized as e:
            return (
                {"message": "Unauthorized."},
                HttpStatus.UNAUTHORIZED.value,
            )
        except Exception as e:
            LoggerSetup.get_logger("general").error(
                f"Internal server error while toggling user status with ID:{user_id}, err : {e}"
            )
            return (
                {"message": f"Internal server error: {str(e)}"},
                HttpStatus.INTERNAL_SERVER_ERROR.value,
            )


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
        current_user_id = get_jwt_identity()

        try:
            current_user = UserCRUDService.get_user(current_user_id)
            if not UserAuthService.check_if_admin(current_user):
                return {"message": "Unauthorized"}, HttpStatus.UNAUTHORIZED.value

            user = UserCRUDService.get_user(user_id)
            data = request.json
            UserAuthService.change_password(user, data.get("new_password"))

            return {"message": "Password changed successfully"}, HttpStatus.OK.value

        except DoesNotExist:
            return {"message": "User not found"}, HttpStatus.NOT_FOUND.value

        except Exception as e:
            return {
                "message": f"Internal server error: {str(e)}"
            }, HttpStatus.INTERNAL_SERVER_ERROR.value


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
        current_user_id = get_jwt_identity()

        try:
            current_user = UserCRUDService.get_user(current_user_id)
            if not UserAuthService.check_if_admin(current_user):
                return {"message": "Unauthorized"}, HttpStatus.UNAUTHORIZED.value

            filters = json.loads(args["filters"]) if args["filters"] else {}

            users, total_entries, total_pages = UserPaginationService.get_rows(
                page=args["page"],
                per_page=args["per_page"],
                sort_field=args["sort_field"],
                sort_order=args["sort_order"],
                search=args["search"],
                filters=filters,
            )

            return {
                "users": users,
                "total_entries": total_entries,
                "total_pages": total_pages,
            }, HttpStatus.OK.value

        except ValueError as e:
            return {"message": str(e)}, HttpStatus.BAD_REQUEST.value
        except AttributeError as e:
            return {"message": f"Field error: {str(e)}"}, HttpStatus.BAD_REQUEST.value
        except Exception as e:
            return {"message": str(e)}, HttpStatus.INTERNAL_SERVER_ERROR.value
