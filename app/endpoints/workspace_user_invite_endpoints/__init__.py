from flask_restx import Namespace

from app.models.validation_schemas.retrievers.workspace_user_invite_schema_retriever import (
    WorkspaceUserInviteSchemaRetriever,
)


workspace_user_invite_namespace = Namespace(
    "Workspace Invites", description="Workspace invite operations"
)
workspace_user_invite_schema_retriever = WorkspaceUserInviteSchemaRetriever(
    workspace_user_invite_namespace
)

from .user_workspace_user_invite_endpoints import *
