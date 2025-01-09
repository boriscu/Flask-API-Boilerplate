from flask_restx import Namespace

from app.models.validation_schemas.retrievers.workspace_schema_retriever import (
    WorkspaceSchemaRetriever,
)


workspace_namespace = Namespace("Workspaces", description="Workspace operations")
workspace_schema_retriever = WorkspaceSchemaRetriever(workspace_namespace)

from .admin_workspace_endpoints import *
