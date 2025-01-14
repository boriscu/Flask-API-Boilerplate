from app.models.validation_schemas.schemas.workspace_user_invite_schemas.invite_creation_response_schema import (
    get_invite_creation_response_schema,
)
from app.models.validation_schemas.schemas.workspace_user_invite_schemas.invite_creation_schema import (
    get_invite_creation_schema,
)


def create_workspace_user_invite_schemas(namespace):
    return {
        "invite_creation_request": get_invite_creation_schema(namespace),
        "invite_creation_response": get_invite_creation_response_schema(namespace),
    }
