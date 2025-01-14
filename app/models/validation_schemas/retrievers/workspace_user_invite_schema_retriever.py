from app.models.validation_schemas.retrievers.base_schema_retriever import (
    BaseSchemaRetriever,
)
from app.models.validation_schemas.schemas.base_schemas.pagination_parser_schema import (
    create_pagination_parser,
)
from app.models.validation_schemas.schemas.workspace_user_invite_schemas import (
    create_workspace_user_invite_schemas,
)


class WorkspaceUserInviteSchemaRetriever(BaseSchemaRetriever):
    def __init__(self, namespace):
        super().__init__(namespace)
        self.schemas = create_workspace_user_invite_schemas(namespace)
        self.pagination_parser = create_pagination_parser()

    def retrieve(self, key):
        if key == "pagination_parser":
            return self.pagination_parser
        schema = self.schemas.get(key)
        if not schema:
            raise ValueError(f"Schema with key `{key}` not found.")
        return schema
