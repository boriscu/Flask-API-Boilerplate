from flask import request
from flask_restx import Namespace

from app.helpers.pre_request.pre_request_manager import PreRequestManager
from app.models.validation_schemas.retrievers.workspace_schema_retriever import (
    WorkspaceSchemaRetriever,
)
from app.services.user_services.user_verification_service import UserVerificationService


workspace_namespace = Namespace(
    "Workspaces", description="Workspace operations. Requires the user to be activated"
)

workspace_schema_retriever = WorkspaceSchemaRetriever(workspace_namespace)


def workspace_pre_request():
    """Pre-request function to handle access checks for workspace endpoints.

    It uses the `UserVerificationService` to abort the request if the user is not active.
    """

    PreRequestManager.pre_request_handler(
        base_path="/api/v1/workspace",
        pre_request_function=UserVerificationService.abort_if_not_active,
    )


from .user_workspace_endpoints import *
