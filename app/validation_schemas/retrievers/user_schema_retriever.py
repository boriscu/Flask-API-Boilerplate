from flask_restx import Namespace
from app.validation_schemas.retrievers.base_schema_retriever import BaseSchemaRetriever
from app.validation_schemas.schemas.user_schemas.expect.user_expect_models_retriever import (
    UserExpectModelsRetriever,
)
from app.validation_schemas.schemas.user_schemas.response.user_response_models_retriever import (
    UserResponseModelsRetriever,
)


class UserSchemaRetriever(BaseSchemaRetriever):

    def __init__(self):
        self.namespace = Namespace("Users", description="User operations")
        self.expect_retriever = UserExpectModelsRetriever(self.namespace)
        self.response_retriever = UserResponseModelsRetriever(self.namespace)
        self.model_methods = {
            "register": self.expect_retriever.get_register_model,
            "login": self.expect_retriever.get_login_model,
            "change_password": self.expect_retriever.get_change_password_model,
            "admin_change_password": self.expect_retriever.get_admin_change_password_model,
            "pagination_parser": self.expect_retriever.get_pagination_parser_model,
            "user_profile": self.response_retriever.get_user_profile_model,
            "user_profiles": self.response_retriever.get_user_profiles_model,
            "toggle_status": self.response_retriever.get_toggle_status_model,
            "is_admin": self.response_retriever.get_is_admin_model,
            "is_active": self.response_retriever.get_is_active_model,
        }

    def retrieve(self, key: str):
        method = self.model_methods.get(key)
        if not method:
            raise ValueError(f"Model with key '{key}' not found.")
        return method()
