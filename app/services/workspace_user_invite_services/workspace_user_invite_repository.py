from typing import Any, Dict, List, Tuple
from flask import Response
from flask_jwt_extended import get_jwt_identity


from app.helpers.http_response_generator import HttpResponseGenerator
from app.models.enums.http_status import HttpStatus
from app.models.pg.workspace_user import WorkspaceUser
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
        invitor_id = int(get_jwt_identity())
        invited_id, workspace_user_role = (
            WorkspaceUserInviteValidationService.validate_invitation(
                workspace_id=workspace_id, invitor_id=invitor_id, data=data
            )
        )
        if not WorkspaceUserInviteValidationService.check_existing_invitation(
            workspace_id=workspace_id, data=data
        ):
            WorkspaceUserInvite.create(
                invitor_id=invitor_id,
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
        WorkspaceUserInviteRepository._delete_user_invite(
            invite_id, int(get_jwt_identity())
        )
        return HttpResponseGenerator.generate_response(HttpStatus.OK)

    @staticmethod
    def accept_user_invite(invite_id: int) -> Response:
        invite = WorkspaceUserInvite.get_by_id(invite_id)
        user_id = int(get_jwt_identity())

        WorkspaceUser.create(
            workspace=invite.workspace,
            user=user_id,
            workspace_user_role=invite.workspace_user_role,
        )

        WorkspaceUserInviteRepository._delete_user_invite(invite_id, user_id)

        return HttpResponseGenerator.generate_response(HttpStatus.OK)

    @staticmethod
    def _delete_user_invite(invite_id, user_id):
        WorkspaceUserInvite.delete().where(
            (WorkspaceUserInvite.user == user_id)
            & (WorkspaceUserInvite.id == invite_id)
        ).execute()
