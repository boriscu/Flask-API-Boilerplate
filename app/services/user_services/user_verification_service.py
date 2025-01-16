import hashlib
import secrets
from flask import abort, current_app

from app.models.pg.user_profile import UserProfile

from app.models.enums.http_status import HttpStatus

from app.helpers.email.strategies.user_verification_sender import (
    UserVerificationSender,
)


class UserVerificationService:

    @staticmethod
    def request(email: str):

        if not email:
            abort(HttpStatus.BAD_REQUEST.value)

        user = UserProfile.get(UserProfile.email == email)

        if user.is_sso:
            abort(HttpStatus.FORBIDDEN.value)

        token = secrets.token_urlsafe(32)
        hashed_token = UserVerificationService._hash_token(token)

        current_app.redis.setex(
            f"account-verification:{hashed_token}",
            600,
            user.id,
        )

        UserVerificationSender().send_template(email, token)

    @staticmethod
    def submit(token: str):

        if not token:
            abort(HttpStatus.BAD_REQUEST.value)

        hashed_token = UserVerificationService._hash_token(token)

        user_id = current_app.redis.get(f"account-verification:{hashed_token}")

        if not user_id:
            abort(HttpStatus.UNAUTHORIZED.value)

        user = UserProfile.get(UserProfile.id == user_id)
        user.is_active = True
        user.save()

        current_app.redis.delete(f"account-verification:{hashed_token}")

    @staticmethod
    def _hash_token(token):
        return hashlib.sha256(token.encode("utf-8")).hexdigest()
