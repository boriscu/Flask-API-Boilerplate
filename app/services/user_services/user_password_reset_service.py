import hashlib
import secrets
from flask import abort, current_app
from werkzeug.security import generate_password_hash

from app.helpers.email.strategies.password_reset_sender import PasswordResetSender

from app.models.enums.http_status import HttpStatus

from app.models.pg.user_profile import UserProfile


class UserPasswordResetService:
    @staticmethod
    def request(email: str):
        user = UserProfile.get(UserProfile.email == email)

        token = secrets.token_urlsafe(32)
        hashed_token = UserPasswordResetService._hash_token(token)

        current_app.redis.setex(
            f"password-reset:{hashed_token}",
            600,
            user.id,
        )

        email_sender = PasswordResetSender()
        email_sender.send_template(email, token)

    @staticmethod
    def submit(password: str, token: str):

        if not password or not token:
            abort(HttpStatus.BAD_REQUEST.value)

        hashed_token = UserPasswordResetService._hash_token(token)

        user_id = current_app.redis.get(f"password-reset:{hashed_token}")

        if not user_id:
            abort(HttpStatus.UNAUTHORIZED.value)

        user = UserProfile.get_by_id(user_id)
        user.password = generate_password_hash(password)
        user.save()

        current_app.redis.delete(f"password-reset:{hashed_token}")

    @staticmethod
    def _hash_token(token: str):
        return hashlib.sha256(token.encode("utf-8")).hexdigest()
