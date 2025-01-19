from flask_restx import Namespace

from app.helpers.pre_request.pre_request_manager import PreRequestManager
from app.models.validation_schemas.retrievers.user_schema_retriever import (
    UserSchemaRetriever,
)


user_namespace = Namespace("Users", description="User operations")
user_schema_retriever = UserSchemaRetriever(user_namespace)


def user_pre_request():

    PreRequestManager.pre_request_handler(
        base_path="/api/v1/user",
        pre_request_function=UserVerificationService.abort_if_not_active,
        exclusions=["/verify", "/get_myself"],
    )


from .regular_user_endpoints import *
from .admin_user_endpoints import *
