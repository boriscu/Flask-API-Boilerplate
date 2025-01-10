from app.models.validation_schemas.schemas.user_schemas.admin_change_password_schema import (
    get_admin_change_password_schema,
)
from app.models.validation_schemas.schemas.user_schemas.all_users_schema import (
    get_all_users_schema,
)
from app.models.validation_schemas.schemas.user_schemas.change_password_schema import (
    get_change_password_schema,
)
from app.models.validation_schemas.schemas.user_schemas.full_user_schema import (
    get_full_user_schema,
)
from app.models.validation_schemas.schemas.user_schemas.login_request_schema import (
    get_login_request_schema,
)
from app.models.validation_schemas.schemas.user_schemas.login_response_schema import (
    get_login_response_schema,
)
from app.models.validation_schemas.schemas.user_schemas.registration_schema import (
    get_user_registration_schema,
)
from app.models.validation_schemas.schemas.user_schemas.toggle_user_status_response_schema import (
    get_toggle_user_status_response_schema,
)


def create_user_models(namespace):

    return {
        "registration": get_user_registration_schema(),
        "login_request": get_login_request_schema(namespace),
        "login_response": get_login_response_schema(namespace),
        "profile": get_full_user_schema(namespace),
        "toggle_status": get_toggle_user_status_response_schema(namespace),
        "change_password": get_change_password_schema(namespace),
        "admin_change_password": get_admin_change_password_schema(namespace),
        "users_response": get_all_users_schema(namespace),
    }
