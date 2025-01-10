from app.models.validation_schemas.schemas.base_schemas.pagination_parser_schema import (
    create_pagination_parser,
)
from app.models.validation_schemas.schemas.workspace_schemas import (
    create_workspace_models,
)
from app.models.validation_schemas.retrievers.base_schema_retriever import (
    BaseSchemaRetriever,
)


class WorkspaceSchemaRetriever(BaseSchemaRetriever):
    def __init__(self, namespace):
        super().__init__(namespace)
        self.models = create_workspace_models(namespace)
        self.pagination_parser = create_pagination_parser()

    def retrieve(self, key):
        if key == "pagination_parser":
            return self.pagination_parser
        model = self.models.get(key)
        if not model:
            raise ValueError(f"Model with key `{key}` not found.")
        return model
