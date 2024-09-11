from app.validation_schemas.models.user_models import (
    create_pagination_parser,
    create_user_models,
)
from app.validation_schemas.retrievers.base_schema_retriever import BaseSchemaRetriever


class UserSchemaRetriever(BaseSchemaRetriever):
    def __init__(self, namespace):
        super().__init__(namespace)
        self.models = create_user_models(namespace)
        self.pagination_parser = create_pagination_parser()

    def retrieve(self, key: str):
        if key == "pagination_parser":
            return self.pagination_parser
        model = self.models.get(key)
        if not model:
            raise ValueError(f"Model with key '{key}' not found.")
        return model
