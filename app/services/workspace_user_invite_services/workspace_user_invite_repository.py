from typing import Any, Dict
from flask import Response
from flask_jwt_extended import get_jwt_identity


from app.helpers.http_response_generator import HttpResponseGenerator
from app.models.enums.http_status import HttpStatus
from app.models.pg.workspace_user_invite import WorkspaceUserInvite
from app.services.workspace_user_invite_services.workspace_user_invite_validation_service import (
    WorkspaceUserInviteValidationService,
)


class WorkspaceUserInviteRepository:
    @staticmethod
    def create_workspace_user_invite(
        workspace_id: int, data: Dict[str, Any]
    ) -> Response:
        invited_id, workspace_user_role = (
            WorkspaceUserInviteValidationService.validate_invitation(
                workspace_id=workspace_id, invitor_id=int(get_jwt_identity()), data=data
            )
        )

        WorkspaceUserInvite.create(
            workspace=workspace_id,
            user=invited_id,
            workspace_user_role=workspace_user_role.value,
        )

        return HttpResponseGenerator.generate_response(HttpStatus.CREATED)
