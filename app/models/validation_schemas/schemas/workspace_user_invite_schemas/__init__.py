from app.models.validation_schemas.schemas.workspace_user_invite_schemas.invite_accept_by_token_schema import (
    get_user_invite_accept_by_token_schema,
)
from app.models.validation_schemas.schemas.workspace_user_invite_schemas.invite_creation_response_schema import (
    get_invite_creation_response_schema,
)
from app.models.validation_schemas.schemas.workspace_user_invite_schemas.invite_creation_schema import (
    get_invite_creation_schema,
)
from app.models.validation_schemas.schemas.workspace_user_invite_schemas.invites_schema import (
    get_all_invites_schema,
)
from app.models.validation_schemas.schemas.workspace_user_invite_schemas.invitor_schema import (
    get_invitor_schema,
)


def create_workspace_user_invite_schemas(namespace):
    return {
        "invite_creation_request": get_invite_creation_schema(namespace),
        "invite_creation_response": get_invite_creation_response_schema(namespace),
        "invite_accept_by_token": get_user_invite_accept_by_token_schema(namespace),
        "invitor": get_invitor_schema(namespace),
        "invites": get_all_invites_schema(namespace),
    }
