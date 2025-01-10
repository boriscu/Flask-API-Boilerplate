from app.models.validation_schemas.schemas.workspace_schemas.all_workspace_schema import (
    get_all_workspace_schema,
)
from app.models.validation_schemas.schemas.workspace_schemas.create_workspace_response_schema import (
    get_create_workspace_response_schema,
)
from app.models.validation_schemas.schemas.workspace_schemas.full_workspace_schema import (
    get_full_workspace_schema,
)
from app.models.validation_schemas.schemas.workspace_schemas.workspace_creation_schema import (
    get_workspace_creation_schema,
)


def create_workspace_models(namespace):

    return {
        "create_workspace_request": get_workspace_creation_schema(),
        "create_workspace_response": get_create_workspace_response_schema(namespace),
        "workspaces": get_all_workspace_schema(namespace),
        "workspace": get_full_workspace_schema(namespace),
    }
