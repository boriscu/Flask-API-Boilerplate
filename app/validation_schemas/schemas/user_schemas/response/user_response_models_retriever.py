from flask_restx import Namespace

from app.validation_schemas.schemas.base_response_model_retriever import (
    BaseResponseModelRetriever,
)
from app.validation_schemas.schemas.user_schemas.response.models.is_active_model import (
    is_active_model,
)
from app.validation_schemas.schemas.user_schemas.response.models.is_admin_model import (
    is_admin_model,
)
from app.validation_schemas.schemas.user_schemas.response.models.toggle_status_model import (
    toggle_status_model,
)
from app.validation_schemas.schemas.user_schemas.response.models.user_profile_model import (
    user_profile_model,
)
from app.validation_schemas.schemas.user_schemas.response.models.user_profiles_model import (
    user_profiles_model,
)


class UserResponseModelsRetriever(BaseResponseModelRetriever):
    def __init__(self, namespace: Namespace):
        super().__init__(namespace)

    def get_user_profile_model(self):
        return self.add_message_field(user_profile_model)

    def get_user_profiles_model(self):
        return self.add_message_field(user_profiles_model)

    def get_toggle_status_model(self):
        return self.add_message_field(toggle_status_model)

    def get_is_admin_model(self):
        return self.add_message_field(is_admin_model)

    def get_is_active_model(self):
        return self.add_message_field(is_active_model)
