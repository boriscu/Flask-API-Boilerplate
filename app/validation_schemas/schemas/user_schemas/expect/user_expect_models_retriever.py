from flask_restx import Namespace
from app.validation_schemas.schemas.base_expect_model_retriever import (
    BaseExpectModelRetriever,
)
from app.validation_schemas.schemas.user_schemas.expect.models.admin_change_password_model import (
    admin_change_password_model,
)
from app.validation_schemas.schemas.user_schemas.expect.models.change_password_model import (
    change_password_model,
)
from app.validation_schemas.schemas.user_schemas.expect.models.login_model import (
    login_model,
)
from app.validation_schemas.schemas.user_schemas.expect.models.pagination_parser_model import (
    pagination_parser_model,
)
from app.validation_schemas.schemas.user_schemas.expect.models.register_model import (
    register_model,
)


class UserExpectModelsRetriever(BaseExpectModelRetriever):
    def __init__(self, namespace: Namespace):
        super().__init__(namespace)

    def get_register_model(self):
        return self.register_model_to_namespace(register_model)

    def get_pagination_parser_model(self):
        return pagination_parser_model

    def get_login_model(self):
        return self.register_model_to_namespace(login_model)

    def get_change_password_model(self):
        return self.register_model_to_namespace(change_password_model)

    def get_admin_change_password_model(self):
        return self.register_model_to_namespace(admin_change_password_model)
