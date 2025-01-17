from flask_restx import Namespace

from app.models.validation_schemas.retrievers.auth_schema_retriever import (
    AuthSchemaRetriever,
)


auth_namespace = Namespace("Auth", description="Auth operations")
auth_schema_retriever = AuthSchemaRetriever(auth_namespace)

from .regular_auth_endpoints import *
from .admin_auth_endpoints import *
