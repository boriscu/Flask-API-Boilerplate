from typing import Dict, Optional
from app.models.user_profile import UserProfile
from peewee import DoesNotExist, PeeweeException


class UserCRUDService:
    @staticmethod
    def get_user(user_id: int) -> Optional[UserProfile]:
        """
        Retrieves a user by their ID, excluding the password from the output.

        Args:
            user_id (int): The ID of the user to retrieve.

        Returns:
            Optional[UserProfile]: A UserProfile class instance containing current user data if the user exists, None otherwise.

        Raises:
            Exception: An exception indicating an internal server error if a database or unexpected error occurs.
        """
        try:
            return UserProfile.get_by_id(user_id)
        except DoesNotExist:
            return None
        except PeeweeException as e:
            raise Exception("Internal server error occurred.") from e
