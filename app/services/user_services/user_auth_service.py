from typing import Dict, Union
from flask import make_response
from flask_jwt_extended import create_access_token
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import timedelta

from config.app_config import AppConfig

from app.models.enums.http_status import HttpStatus

from app.models.pg.user_profile import UserProfile


class UserAuthService:
    """
    A service class for user authentication, including registration,
    login, util methods.
    """

    @staticmethod
    def register(data: Dict[str, str]) -> Union[Dict[str, str], make_response]:
        """
        Registers a new user with just the required fields (name, surname, email, password)
        and returns a JWT token.

        Args:
            data (dict): A dictionary containing the user's name, surname, email, and password.

        Returns:
            Union[Dict[str, str], make_response]: A response message with the status code and a token.
        """
        name = data.get("name")
        surname = data.get("surname")
        email = data.get("email")
        password = data.get("password")
        is_sso = data.get("is_sso", False)
        hashed_password = generate_password_hash(password)

        user = UserProfile.create(
            name=name,
            surname=surname,
            email=email,
            password=hashed_password,
            is_sso=is_sso,
            is_admin=False,
            is_active=True,
        )
        user.save()

        response = make_response(
            {"message": "User created successfully"},
            HttpStatus.OK.value,
        )
        return response

    @staticmethod
    def login(data: Dict[str, str]) -> Union[Dict[str, str], make_response]:
        """
        Logs in a user by validating the email and password.

        Args:
            data (dict): A dictionary containing the user's email and password.

        Returns:
            Union[Dict[str, str], make_response]: A success or error message with the status code.
        """
        email = data.get("email")
        password = data.get("password")

        user = UserProfile.get(UserProfile.email == email)

        if check_password_hash(user.password, password):
            access_token = create_access_token(
                identity=str(user.id),
                expires_delta=timedelta(minutes=int(AppConfig.TOKEN_EXPIRATION_TIME)),
            )

            response = make_response(
                {
                    "message": "Login successful",
                    "access_token": access_token,
                },
                HttpStatus.OK.value,
            )
            return response
        else:
            return {"message": "Password is incorrect"}, HttpStatus.UNAUTHORIZED.value

    @staticmethod
    def check_if_admin(user: UserProfile) -> bool:
        """
        Checks if the UserProfile instance is an admin

        Returns:
            bool: True if the user is admin, false in other case
        """
        return user.is_admin

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
