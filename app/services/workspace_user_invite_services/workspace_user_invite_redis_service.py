import hashlib
from flask import current_app


class WorkspaceUserInviteRedisService:
    @staticmethod
    def get_invite(token: str) -> bytes | None:
        return current_app.redis.get(f"workspace-invite:{token}")

    @staticmethod
    def save_invite(token: str, for_how_long: int, value: any) -> None:
        current_app.redis.setex(f"workspace-invite:{token}", for_how_long, value)

    @staticmethod
    def delete_invite(token: str) -> None:
        current_app.redis.delete(f"workspace-invite:{token}")

    @staticmethod
    def hash_token(token: str) -> str:
        return hashlib.sha256(token.encode("utf-8")).hexdigest()
