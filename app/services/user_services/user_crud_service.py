from typing import Dict, Optional, Tuple
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
            raise
        except PeeweeException as e:
            raise Exception("Internal server error occurred.") from e

    @staticmethod
    def toggle_active_status(user: UserProfile) -> Tuple[bool, str]:
        """
        Toggles the active status of a user. If the user is currently active, they will be set to inactive,
        and if inactive, they will be set to active.

        Args:
            user (UserProfile): The user profile whose status is to be toggled.

        Returns:
            Tuple[bool, str]: A tuple containing a boolean indicating the new active status and a message about the update.
        """
        try:
            if user.is_active:
                user.is_active = False
                message = "User status changed to inactive."
            else:
                user.is_active = True
                message = "User status changed to active."

            user.save()
            return user.is_active, message
        except Exception as e:
            raise Exception(f"Error while toggling user status: {str(e)}")
