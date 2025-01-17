import json
from typing import Dict, Any

from flask import current_app

from app.services.workspace_user_invite_services.workspace_user_invite_repository import (
    WorkspaceUserInviteRepository,
)


class WorkspaceNonRegistredUserInviteService:
    @staticmethod
    def reserve_invite(workspace_id: int, data: Dict[str, Any]) -> None:
        invite = current_app.redis.get(f"workspace-invite:{data['user_email']}")

        if invite:
            invite = json.loads(invite)
            if not invite["workspace_id"] == workspace_id:
                new_invite = data
                new_invite["workspace_id"] = workspace_id
                current_app.redis.setex(
                    data["user_email"], 60 * 60 * 24, json.dumps(new_invite)
                )

        else:
            invite = data
            invite["workspace_id"] = workspace_id
            current_app.redis.setex(
                f"workspace-invite:{data['user_email']}",
                60 * 60 * 24,
                json.dumps(invite),
            )

    @staticmethod
    def invite_if_exists(email: str) -> None:
        invite = current_app.redis.get(email)

        if invite:
            invite = json.loads(invite)
            current_app.redis.delete(email)

            return WorkspaceUserInviteRepository.create_workspace_user_invite(
                invite["workspace_id"],
                {k: invite[k] for k in invite.keys() if k != "workspace_id"},
            )
