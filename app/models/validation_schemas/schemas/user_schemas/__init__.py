from app.models.validation_schemas.schemas.user_schemas.all_users_schema import (
    get_all_users_schema,
)
from app.models.validation_schemas.schemas.auth_schemas.change_password_schema import (
    get_change_password_schema,
)
from app.models.validation_schemas.schemas.user_schemas.full_user_schema import (
    get_full_user_schema,
)
from app.models.validation_schemas.schemas.user_schemas.toggle_user_status_response_schema import (
    get_toggle_user_status_response_schema,
)
from app.models.validation_schemas.schemas.user_schemas.update_user_schema import (
    get_update_user_schema,
)
from app.models.validation_schemas.schemas.user_schemas.user_verification_schema import (
    get_user_verification_schema,
)
from app.models.validation_schemas.schemas.user_schemas.verification_response_schema import (
    get_verification_response_schema,
)


def create_user_schemas(namespace):

    return {
        "profile": get_full_user_schema(namespace),
        "toggle_status": get_toggle_user_status_response_schema(namespace),
        "users_response": get_all_users_schema(namespace),
        "update_user": get_update_user_schema(namespace),
        "user_verification": get_user_verification_schema(namespace),
        "verification_response": get_verification_response_schema(namespace),
    }
