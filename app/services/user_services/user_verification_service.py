from datetime import timedelta
import hashlib
import secrets
from flask import abort, current_app
from flask_jwt_extended import create_access_token, get_jwt, verify_jwt_in_request

from config.app_config import AppConfig

from app.models.enums.http_status import HttpStatus

from app.models.pg.user_profile import UserProfile

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
    def re_request(user_id: int):

        user = UserProfile.get_by_id(user_id)

        if user.is_active or user.is_sso:
            abort(HttpStatus.BAD_REQUEST.value)

        token = secrets.token_urlsafe(32)
        hashed_token = UserVerificationService._hash_token(token)

        current_app.redis.setex(
            f"account-verification:{hashed_token}",
            600,
            user.id,
        )

        UserVerificationSender().send_template(user.email, token)

    @staticmethod
    def submit(token: str) -> str:
        """Verifies the user and returns the access token with updated access rights

        Args:
            token (str): Received verification token to be checked against the one in Redis

        Returns:
            access_token (str): New access token
        """
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

        access_token = create_access_token(
            identity=str(user.id),
            expires_delta=timedelta(minutes=int(AppConfig.TOKEN_EXPIRATION_TIME)),
            additional_claims={
                "is_admin": user.is_admin,
                "is_active": user.is_active,
            },
        )

        return access_token

    @staticmethod
    def abort_if_not_active():
        """Abort the request if the user is not considered active based on JWT.

        This function verifies the JWT in the request and aborts the request with a 423 (Locked) status
        if the 'is_active' claim in the JWT is False.
        """
        try:
            verify_jwt_in_request()
            if not get_jwt().get("is_active"):
                abort(HttpStatus.RESOURCE_LOCKED.value)
        except:
            abort(HttpStatus.RESOURCE_LOCKED.value)

    @staticmethod
    def _hash_token(token):
        return hashlib.sha256(token.encode("utf-8")).hexdigest()
