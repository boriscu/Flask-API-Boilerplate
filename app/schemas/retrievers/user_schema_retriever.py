from app.schemas.models.user_models import create_user_models
from app.schemas.retrievers.base_schema_retriever import BaseSchemaRetriever


class UserSchemaRetriever(BaseSchemaRetriever):
    def __init__(self, namespace):
        super().__init__(namespace)
        self.models = create_user_models(namespace)

    def retrieve(self, key: str):
        model = self.models.get(key)
        if not model:
            raise ValueError(f"Model with key '{key}' not found.")
        return model
