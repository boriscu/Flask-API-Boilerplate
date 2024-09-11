from flask_restx import Namespace

from app.validation_schemas.retrievers.user_schema_retriever import UserSchemaRetriever

user_schema_retriever = UserSchemaRetriever()
user_namespace = user_schema_retriever.namespace

from .regular_user_endpoints import *
from .admin_user_endpoints import *
