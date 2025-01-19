import json
from flask import current_app

from app.services.workspace_user_invite_services.workspace_user_invite_repository import (
    WorkspaceUserInviteRepository,
)


class WorkspaceUserInviteSyncEngine:
    @staticmethod
    def sync(email: str) -> None:
        cursor = 0
        while True:
            cursor, keys = current_app.redis.scan(
                cursor=cursor,
                match=f"workspace-invite:{email}:*",
            )

            for key in keys:
                value = json.loads(current_app.redis.get(key))

                WorkspaceUserInviteRepository.create_workspace_user_invite(
                    workspace_id=value["workspace_id"],
                    invitor_id=value["invitor_id"],
                    data=value["data"],
                )

            if cursor == 0:
                break
