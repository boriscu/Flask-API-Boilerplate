import json

from flask import current_app

from app.services.workspace_user_invite_services.workspace_user_invite_repository import (
    WorkspaceUserInviteRepository,
)


class WorkspaceNonRegistredUserInviteService:
    @staticmethod
    def invite_if_exists(email: str):
        invite = current_app.redis.get(email)

        if invite:
            invite = json.loads(invite)

            current_app.redis.delete(email)

            return WorkspaceUserInviteRepository.create_workspace_user_invite(
                invite["workspace_id"],
                {k: invite[k] for k in invite.keys() if k != "workspace_id"},
            )
