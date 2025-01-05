from app.models.validation_schemas.models.workspace_models import (
    create_workspace_models,
)
from app.models.validation_schemas.retrievers.base_schema_retriever import (
    BaseSchemaRetriever,
)


class WorkspaceSchemaRetriever(BaseSchemaRetriever):
    def __init__(self, namespace):
        super().__init__(namespace)
        self.models = create_workspace_models(namespace)

    def retrieve(self, key):
        model = self.models.get(key)
        if not model:
            raise ValueError(f"Model with key `{key}` not found.")
        return model
