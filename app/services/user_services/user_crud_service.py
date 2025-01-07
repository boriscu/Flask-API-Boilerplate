from typing import Dict, List, Tuple, Union
from flask import json


from app.models.pg.user_profile import UserProfile

from app.services.user_services.user_auth_service import UserAuthService
from app.services.user_services.user_pagination_service import UserPaginationService


class UserCRUDService:
    @staticmethod
    def get_single_user(user_id: int) -> UserProfile:
        """
        Retrieves a user by their ID. Requires admin privileges

        Args:
            user_id (int): The ID of the user to retrieve.

        Returns:
            Optional[UserProfile]: A UserProfile class instance containing current user data if the user exists, None otherwise.

        """
        UserAuthService.check_if_admin()
        return UserProfile.get_by_id(user_id)

    @staticmethod
    def get_all_users(args: dict) -> Tuple[List[UserProfile], int, int]:
        """
        Retrieves all users with pagination, sorting, searching, and filtering options based on given parameters.

        Args:
            args (Dict[str, str]): A dictionary containing the parameters for pagination, sorting, searching, and filtering:
                - "page" (str): The page number as a string.
                - "per_page" (str): The number of users to display per page as a string.
                - "sort_field" (str): The field by which to sort the user results.
                - "sort_order" (str): The order of sorting, either 'asc' for ascending or 'desc' for descending.
                - "search" (str): The search term used to filter results.
                - "filters" (str): A JSON string representing additional filters to apply.

        Returns:
            Tuple[List[UserProfile], int, int]: A tuple containing a list of UserProfile objects, the total number of users,
                                               and the total number of pages available based on the given parameters.

        Raises:
            ValueError: If JSON decoding fails for filters.
        """

        UserAuthService.check_if_admin()

        return UserPaginationService.get_rows(
            page=args["page"],
            per_page=args["per_page"],
            sort_field=args["sort_field"],
            sort_order=args["sort_order"],
            search=args["search"],
            filters=json.loads(args["filters"]) if args["filters"] else {},
        )

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
        if user.is_active:
            user.is_active = False
            message = "User status changed to inactive."
        else:
            user.is_active = True
            message = "User status changed to active."

        user.save()
        return user.is_active, message

    @staticmethod
    def update_user_password(
        user: UserProfile, old_password: str, new_password: str
    ) -> Union[Dict[str, str], None]:
        """
        Changes the password for a user after validating the old password.

        Args:
            user (UserProfile): The user whose password is to be changed.
            old_password (str): The current password to verify.
            new_password (str): The new password to set.

        Returns:
            Union[Dict[str, str], None]: A message dictionary in case of an error, None if the password was updated.
        """
        if not UserAuthService.check_password(user, old_password):
            return {"msg": "Old password is incorrect"}

        UserAuthService.change_password(user, new_password)
        return None
