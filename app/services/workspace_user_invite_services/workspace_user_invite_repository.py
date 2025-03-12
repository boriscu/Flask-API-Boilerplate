import hashlib
import json
from typing import Any, Dict, List, Tuple
from flask import Response, abort
from flask_jwt_extended import get_jwt_identity

from app.models.enums.http_status import HttpStatus

from app.models.pg.workspace_user import WorkspaceUser
from app.models.pg.workspace_user_invite import WorkspaceUserInvite
from app.models.pg.user_profile import UserProfile

from app.helpers.email.strategies.workspace_invite_sender import WorkspaceInviteSender

from app.services.workspace_user_invite_services.workspace_user_invite_pagination_service import (
    WorkspaceUserInvitePaginationService,
)
from app.services.workspace_user_invite_services.workspace_user_invite_redis_service import (
    WorkspaceUserInviteRedisService,
)
from app.services.workspace_user_invite_services.workspace_user_invite_validation_service import (
    WorkspaceUserInviteValidationService,
)


class WorkspaceUserInviteRepository:
    @staticmethod
    def create_workspace_user_invite(
        workspace_id: int, invitor_id: int, data: Dict[str, Any]
    ) -> Response:
        user_email = data.get("user_email")

        already_invited_redis, hashed_token = (
            WorkspaceUserInviteRepository.__save_invite_to_redis(
                workspace_id=workspace_id, invitor_id=invitor_id, data=data
            )
        )

        invited_user = UserProfile.get_or_none(UserProfile.email == user_email)

        if invited_user is not None:
            invited_id, workspace_user_role = (
                WorkspaceUserInviteValidationService.validate_invitation(
                    workspace_id=workspace_id,
                    invitor_id=invitor_id,
                    invited_user=invited_user,
                    data=data,
                )
            )
            if not WorkspaceUserInviteValidationService.check_existing_invitation(
                workspace_id=workspace_id, invited_id=invited_id
            ):
                WorkspaceUserInvite.create(
                    invitor_id=invitor_id,
                    workspace=workspace_id,
                    user=invited_id,
                    workspace_user_role=workspace_user_role.value,
                )

        if not already_invited_redis:
            WorkspaceInviteSender().send_template(
                user_email=user_email,
                token=hashed_token,
            )

    @staticmethod
    def __save_invite_to_redis(
        workspace_id: int, invitor_id: int, data: Dict[str, Any]
    ) -> Tuple[bool, str]:
        user_email = data.get("user_email")
        print(user_email)

        hashed_token = WorkspaceUserInviteRedisService.hash_token(
            f"{user_email}:{workspace_id}"
        )

        invite = WorkspaceUserInviteRedisService.get_invite(
            f"{user_email}:{hashed_token}"
        )

        if invite is None:
            WorkspaceUserInviteRedisService.save_invite(
                f"{user_email}:{hashed_token}",
                60 * 60 * 24,
                json.dumps(
                    {
                        "workspace_id": workspace_id,
                        "invitor_id": invitor_id,
                        "data": data,
                    }
                ),
            )

        return invite is not None, hashed_token

    @staticmethod
    def get_all_invites(args: dict) -> Tuple[List[WorkspaceUserInvite], int, int]:
        return WorkspaceUserInvitePaginationService.get_serialized_invites(args)

    @staticmethod
    def decline_user_invite(invite_id: int) -> Response:
        WorkspaceUserInviteRepository._delete_user_invite(
            invite_id, int(get_jwt_identity())
        )

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

    @staticmethod
    def accept_user_invite_by_token(request_data: dict[str, any]):
        invite_email = request_data["invite_email"]
        invite_token = request_data["invite_token"]
        key = f"{invite_email}:{invite_token}"

        invite = WorkspaceUserInviteRedisService.get_invite(key)

        if not invite:
            abort(HttpStatus.NOT_FOUND.value)

        invite_value = json.loads(invite)

        data = invite_value["data"]
        workspace_id = invite_value["workspace_id"]

        user_id = UserProfile.get(UserProfile.email == data["user_email"]).id

        invite_id = WorkspaceUserInvite.get(
            WorkspaceUserInvite.id == workspace_id
            and WorkspaceUserInvite.user == user_id
        ).id

        WorkspaceUserInviteRedisService.delete_invite(key)

        WorkspaceUserInviteRepository.accept_user_invite(invite_id)

    @staticmethod
    def _delete_user_invite(invite_id, user_id):
        WorkspaceUserInvite.delete().where(
            (WorkspaceUserInvite.user == user_id)
            & (WorkspaceUserInvite.id == invite_id)
        ).execute()

    @staticmethod
    def _hash_token(token):
        return hashlib.sha256(token.encode("utf-8")).hexdigest()
