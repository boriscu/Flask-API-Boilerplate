from app.models.validation_schemas.schemas.auth_schemas.admin_change_password_schema import (
    get_admin_change_password_schema,
)
from app.models.validation_schemas.schemas.auth_schemas.change_password_schema import (
    get_change_password_schema,
)
from app.models.validation_schemas.schemas.auth_schemas.login_request_schema import (
    get_login_request_schema,
)
from app.models.validation_schemas.schemas.auth_schemas.login_response_schema import (
    get_login_response_schema,
)
from app.models.validation_schemas.schemas.auth_schemas.password_reset_request_schema import (
    get_password_reset_request_schema,
)
from app.models.validation_schemas.schemas.auth_schemas.password_reset_submit_schema import (
    get_password_reset_submit_schema,
)
from app.models.validation_schemas.schemas.auth_schemas.registration_schema import (
    get_user_registration_schema,
)


def create_auth_schemas(namespace):

    return {
        "admin_change_password": get_admin_change_password_schema(namespace),
        "login_request": get_login_request_schema(namespace),
        "login_response": get_login_response_schema(namespace),
        "registration": get_user_registration_schema(),
        "change_password": get_change_password_schema(namespace),
        "change_password": get_change_password_schema(namespace),
        "password_reset_request": get_password_reset_request_schema(namespace),
        "password_reset_submit": get_password_reset_submit_schema(namespace),
    }
