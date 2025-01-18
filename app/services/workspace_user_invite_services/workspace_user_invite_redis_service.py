import hashlib
import json
from flask import current_app

from app.services.workspace_user_invite_services.workspace_user_invite_repository import (
    WorkspaceUserInviteRepository,
)


class WorkspaceUserInviteRedisService:
    @staticmethod
    def get_invite(token: str) -> bytes | None:
        return current_app.redis.get(f"workspace-invite:{token}")

    @staticmethod
    def save_invite(token: str, for_how_long: int, value: any) -> None:
        current_app.redis.setex(f"workspace-invite:{token}", for_how_long, value)

    @staticmethod
    def hash_token(token: str) -> str:
        return hashlib.sha256(token.encode("utf-8")).hexdigest()

    @staticmethod
    def sync_with_pg(email: str) -> None:
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
                    data=value["data"],
                )
            if cursor == 0:
                break
