from typing import Any, Dict, Optional
from flask import abort
from flask_jwt_extended import create_access_token, get_jwt, verify_jwt_in_request
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import timedelta

from config.app_config import AppConfig

from app.models.enums.http_status import HttpStatus

from app.models.pg.user_profile import UserProfile

from app.helpers.validators.date_validator import DateValidator
from app.helpers.validators.password_validator import PasswordValidator
from app.helpers.image_processor import ImageProcessor

from app.services.user_services.user_verification_service import (
    UserVerificationService,
)
from app.services.workspace_user_services.workspace_user_repository import (
    WorkspaceUserRepository,
)


class UserAuthService:
    """
    A service class for user authentication, including registration,
    login, util methods.
    """

    def register(args: Dict[str, Any]) -> str:
        """
        Registers a new user with the required and optional fields, handles SSO based on admin rights,
        and returns a consistent response format with an access token, which is empty if registered by an admin.

        Args:
            args (Dict[str, Union[str, bool, None]]): A dictionary containing the user's registration information:
                - name (str): User's first name.
                - surname (str): User's last name.
                - email (str): User's unique email address.
                - password (str): User's password.
                - birthday (str, optional): User's date of birth.
                - sex (str, optional): User's sex.
                - profession (str, optional): User's profession.
                - is_active(bool, optional): Flag indicating if the user account is activated (only modifiable by admins).
                - is_sso (bool, optional): Flag indicating if the user is using SSO (only modifiable by admins).

        Returns:
            access_token (str)
        """

        name = args.get("name")
        surname = args.get("surname")
        email = args.get("email")
        password = PasswordValidator.validate_password(args.get("password"))
        birthday = DateValidator.date_from_string(args.get("birthday", None))
        sex = args.get("sex", None)
        profession = args.get("profession", None)
        profile_picture = args.get("profile_picture", None)
        profile_picture_data = (
            ImageProcessor.compress_image(profile_picture) if profile_picture else None
        )

        is_admin = UserAuthService.check_if_admin()

        is_sso = args.get("is_sso", False) if is_admin else False
        is_active = args.get("is_sso", False) if is_admin else False

        hashed_password = generate_password_hash(password)

        user = UserProfile.create(
            name=name,
            surname=surname,
            email=email,
            password=hashed_password,
            birthday=birthday,
            sex=sex,
            profession=profession,
            profile_picture=profile_picture_data,
            is_sso=is_sso,
            is_admin=False,
            is_active=is_active,
        )

        WorkspaceUserRepository.create_personal_workspace(name, user.id)

        from app.services.workspace_user_invite_services.workspace_user_invite_sync_engine import (
            WorkspaceUserInviteSyncEngine,
        )

        WorkspaceUserInviteSyncEngine.sync(email)

        access_token = ""
        if not is_admin:
            access_token = create_access_token(
                identity=str(user.id),
                expires_delta=timedelta(minutes=int(AppConfig.TOKEN_EXPIRATION_TIME)),
                additional_claims={
                    "is_admin": user.is_admin,
                    "is_active": user.is_active,
                },
            )

        UserVerificationService.request(email)

        return access_token

    @staticmethod
    def login(data: Dict[str, str]) -> Optional[str]:
        """
        Logs in a user by validating the email and password.

        Args:
            data (dict): A dictionary containing the user's email and password.

        Returns:
            access_token (Optional[str]): Access token if password is correct, else None
        """
        email = data.get("email")
        password = data.get("password")

        user = UserProfile.get(UserProfile.email == email)

        if check_password_hash(user.password, password):
            access_token = create_access_token(
                identity=str(user.id),
                expires_delta=timedelta(minutes=int(AppConfig.TOKEN_EXPIRATION_TIME)),
                additional_claims={
                    "is_admin": user.is_admin,
                    "is_active": user.is_active,
                },
            )

            return access_token
        else:
            return None

    @staticmethod
    def check_if_admin() -> bool:
        """
        Check if the current user is an admin based on the JWT token.

        Returns:
            bool: True if the user is an admin, False otherwise.

        Notes:
            If the JWT verification fails or the 'is_admin' field is not present,
            the method will return False.
        """

        try:
            verify_jwt_in_request()
            is_admin = bool(get_jwt().get("is_admin"))
        except Exception as _:
            is_admin = False

        return is_admin

    @staticmethod
    def check_if_admin_and_raise():
        """
        Validates if the current user token has admin privileges. If the user is not an admin,
        the method aborts the process by sending a 403 Forbidden HTTP status.

        Raises:
            HTTPException: A 403 Forbidden status if the user is not an admin.
        """
        if not UserAuthService.check_if_admin():
            abort(HttpStatus.FORBIDDEN.value)

    @staticmethod
    def check_password(user: UserProfile, password: str) -> bool:
        """
        Checks if the provided password matches the current password of the user.

        Args:
            user (UserProfile): The user whose password is being checked.
            password (str): The password to verify.

        Returns:
            bool: True if the password matches, False otherwise.
        """
        return check_password_hash(user.password, password)

    @staticmethod
    def change_password(user: UserProfile, new_password: str) -> None:
        """
        Changes the password for a user to a new one.

        Args:
            user (UserProfile): The user whose password is to be changed.
            new_password (str): The new password to set.

        Returns:
            None
        """
        hashed_password = generate_password_hash(new_password)
        user.password = hashed_password
        user.save()
