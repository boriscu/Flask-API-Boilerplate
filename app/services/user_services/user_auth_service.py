from typing import Dict, Union
from flask import make_response
from werkzeug.security import generate_password_hash, check_password_hash
from peewee import IntegrityError
from flask_jwt_extended import create_access_token, jwt_required
from datetime import timedelta
from app.enums.http_status import HttpStatus
from app.logger_setup import LoggerSetup
from app.models.user_profile import UserProfile
from config.app_config import AppConfig


class UserAuthService:
    """
    A service class for user authentication, including registration,
    login, and logout and util methods.
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
        hashed_password = generate_password_hash(password)

        try:
            user = UserProfile.create(
                name=name,
                surname=surname,
                email=email,
                password=hashed_password,
                is_admin=False,
            )
            user.save()

            access_token = create_access_token(
                identity=user.id,
                expires_delta=timedelta(minutes=int(AppConfig.TOKEN_EXPIRATION_TIME)),
            )

            response = make_response(
                {"message": "User created successfully", "access_token": access_token},
                HttpStatus.OK.value,
            )
            response.set_cookie("access_token_cookie", access_token, httponly=True)
            return response

        except IntegrityError:
            return {
                "message": "This email is already used"
            }, HttpStatus.BAD_REQUEST.value
        except Exception as e:
            LoggerSetup.get_logger("general").error(
                f"Internal server error while registering a user with email:{data['email']}, err: {e}"
            )
            return {
                "message": "Internal server error"
            }, HttpStatus.INTERNAL_SERVER_ERROR.value

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

        try:
            user = UserProfile.get(UserProfile.email == email)
            if check_password_hash(user.password, password):
                access_token = create_access_token(
                    identity=user.id,
                    expires_delta=timedelta(
                        minutes=int(AppConfig.TOKEN_EXPIRATION_TIME)
                    ),
                )

                response = make_response(
                    {"message": "Login successful"}, HttpStatus.OK.value
                )
                response.set_cookie("access_token_cookie", access_token, httponly=True)
                return response
            else:
                return {
                    "message": "Password is incorrect"
                }, HttpStatus.UNAUTHORIZED.value

        except UserProfile.DoesNotExist:
            return {"message": "User not found"}, HttpStatus.NOT_FOUND.value
        except Exception as e:
            LoggerSetup.get_logger("general").error(
                f"Internal server error while attempting login for email:{data['email']}, err: {e}"
            )
            return {
                "message": "Internal server error"
            }, HttpStatus.INTERNAL_SERVER_ERROR.value

    @staticmethod
    @jwt_required()
    def logout() -> make_response:
        """
        Logs out the current user by removing the access token cookie.

        Returns:
            make_response: A success message confirming the logout.
        """
        response = make_response(
            {"message": "User logged out successfully"}, HttpStatus.OK.value
        )
        response.set_cookie("access_token_cookie", "", expires=0, httponly=True)
        return response

    @staticmethod
    def check_if_admin(user: UserProfile) -> bool:
        """
        Checks if the UserProfile instance is an admin

        Returns:
            bool: True if the user is admin, false in other case
        """
        return user.is_admin
