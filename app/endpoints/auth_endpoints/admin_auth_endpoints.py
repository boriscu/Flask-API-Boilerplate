from flask import request
from flask_jwt_extended import jwt_required
from flask_restx import Resource

from app.helpers.validators.password_validator import PasswordValidator
from app.models.enums.http_status import HttpStatus

from app.helpers.http_response_generator import HttpResponseGenerator

from app.services.user_services.user_auth_service import UserAuthService
from app.services.user_services.user_repository import UserRepository

from . import auth_namespace, auth_schema_retriever


@auth_namespace.route("/<int:user_id>", methods=["PUT"])
class AdminPasswordEndpoint(Resource):
    @auth_namespace.doc(
        description="Allows an admin to change the password for a specified user by user ID. Requires admin privileges."
    )
    @auth_namespace.expect(
        auth_schema_retriever.retrieve("admin_change_password"), validate=True
    )
    @auth_namespace.response(HttpStatus.OK.value, "Password changed successfully.")
    @auth_namespace.response(HttpStatus.UNAUTHORIZED.value, "Unauthorized.")
    @jwt_required()
    def put(self, user_id):
        user = UserRepository.get_single_user(user_id, check_admin=True)
        password = PasswordValidator.validate_password(request.json.get("new_password"))

        UserAuthService.change_password(user, password)

        return HttpResponseGenerator.generate_response(HttpStatus.OK)
