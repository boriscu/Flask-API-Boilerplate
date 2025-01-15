from typing import Any, Dict, List, Tuple
from flask import Response
from flask_jwt_extended import get_jwt_identity


from app.helpers.http_response_generator import HttpResponseGenerator
from app.models.enums.http_status import HttpStatus
from app.models.pg.workspace_user_invite import WorkspaceUserInvite
from app.services.workspace_user_invite_services.workspace_user_invite_pagination_service import (
    WorkspaceUserInvitePaginationService,
)
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

    @staticmethod
    def get_all_invites(args: dict) -> Tuple[List[WorkspaceUserInvite], int, int]:
        return WorkspaceUserInvitePaginationService.get_serialized_invites(args)

    @staticmethod
    def decline_user_invite(invite_id: int) -> Response:
        WorkspaceUserInvite.delete().where(
            (WorkspaceUserInvite.user == int(get_jwt_identity()))
            & (WorkspaceUserInvite.id == invite_id)
        ).execute()
        return HttpResponseGenerator.generate_response(HttpStatus.OK)
