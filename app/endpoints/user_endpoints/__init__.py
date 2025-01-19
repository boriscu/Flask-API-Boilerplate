from flask_restx import Namespace

from app.models.validation_schemas.retrievers.user_schema_retriever import (
    UserSchemaRetriever,
)


user_namespace = Namespace("Users", description="User operations")
user_schema_retriever = UserSchemaRetriever(user_namespace)


def user_before_request():
    base_path = "api/v1/user"
    exclusions = ["/verify", "/get_myself"]

    # Prepend the base path to each exclusion path
    full_exclusions = [base_path + exc for exc in exclusions]

    # Check if the path starts with the base path and is not in the exclusions list
    if request.path.startswith(base_path) and not any(
        request.path.startswith(exc) for exc in full_exclusions
    ):
        print(
            "User-specific checks that do not apply to verify or get_myself endpoints..."
        )


from .regular_user_endpoints import *
from .admin_user_endpoints import *
