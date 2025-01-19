from flask_restx import Namespace

from app.helpers.pre_request.pre_request_manager import PreRequestManager

from app.models.validation_schemas.retrievers.workspace_user_invite_schema_retriever import (
    WorkspaceUserInviteSchemaRetriever,
)

from app.services.user_services.user_verification_service import UserVerificationService


workspace_user_invite_namespace = Namespace(
    "Workspace Invites",
    description="Workspace invite operations. Requires the user to be activated",
)
workspace_user_invite_schema_retriever = WorkspaceUserInviteSchemaRetriever(
    workspace_user_invite_namespace
)


def workspace_invite_pre_request():

    PreRequestManager.pre_request_handler(
        base_path="/api/v1/invite",
        pre_request_function=UserVerificationService.abort_if_not_active,
    )


from .user_workspace_user_invite_endpoints import *
