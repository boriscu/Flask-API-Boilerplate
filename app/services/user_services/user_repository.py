from typing import Any, Dict, List, Tuple, Union
from flask import Response, abort, json

from app.models.enums.http_status import HttpStatus

from app.models.pg.user_profile import UserProfile

from app.helpers.image_processor import ImageProcessor
from app.helpers.validators.date_validator import DateValidator
from app.helpers.http_response_generator import HttpResponseGenerator

from app.services.user_services.user_auth_service import UserAuthService
from app.services.user_services.user_pagination_service import UserPaginationService


class UserRepository:

    @staticmethod
    def get_single_user(user_id: int, check_admin: bool = False) -> UserProfile:
        """
        Retrieves a user by their ID. Requires admin privileges

        Args:
            user_id (int): The ID of the user to retrieve.
            check_admin (bool): A flag that instructs admin check

        Returns:
            Optional[UserProfile]: A UserProfile class instance containing current user data if the user exists, None otherwise.

        """
        if check_admin:
            UserAuthService.check_if_admin_and_raise()

        user_profile = UserProfile.get_by_id(user_id)

        if user_profile.profile_picture:
            encoded_image = ImageProcessor.encode_image(user_profile.profile_picture)
            user_profile.profile_picture = encoded_image

        return user_profile

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

        UserAuthService.check_if_admin_and_raise()

        return UserPaginationService.get_rows(
            page=args["page"],
            per_page=args["per_page"],
            sort_field=args["sort_field"],
            sort_order=args["sort_order"],
            search=args["search"],
            filters=json.loads(args["filters"]) if args["filters"] else None,
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
            raise ValueError("Old password is incorrect")

        UserAuthService.change_password(user, new_password)

    @staticmethod
    def delete_user(user_id: int):
        UserAuthService.check_if_admin_and_raise()

        user = UserProfile.get_by_id(user_id)
        if not user.is_admin:
            UserProfile.delete().where(UserProfile.id == user_id).execute()
        else:
            return HttpResponseGenerator.generate_response(HttpStatus.FORBIDDEN)

        return HttpResponseGenerator.generate_response(HttpStatus.OK)

    @staticmethod
    def update_user(user_id: int, args: Dict[str, Any]) -> Response:
        """Update an existing user in the database and return a Flask response object.

        Args:
            user_id (int): The ID of the user to update.
            args (Dict[str, Any]): A dictionary containing user attributes.

        Returns:
            Response: Flask response object with the update status.

        Note: A regular user can only update himself. The is_sso, workspace_creation_quota fields are editable only by admin
        """
        user = UserProfile.get_by_id(user_id)

        if not UserAuthService.check_if_admin() and user.id != user_id:
            abort(HttpStatus.FORBIDDEN.value)

        user.name = args["name"] if args.get("name") is not None else user.name
        user.surname = (
            args["surname"] if args.get("surname") is not None else user.surname
        )
        user.birthday = (
            DateValidator.date_from_string(args["birthday"])
            if args.get("birthday") is not None
            else user.birthday
        )
        user.profession = (
            args["profession"]
            if args.get("profession") is not None
            else user.profession
        )
        user.sex = args["sex"] if args.get("sex") is not None else user.sex

        profile_picture = args.get("profile_picture", None)
        profile_picture_data = (
            ImageProcessor.compress_image(profile_picture) if profile_picture else None
        )
        user.profile_picture = profile_picture_data

        if UserAuthService.check_if_admin():
            user.is_sso = (
                args["is_sso"] if args.get("is_sso") is not None else user.is_sso
            )
            user.workspace_creation_quota = (
                args["workspace_creation_quota"]
                if args.get("workspace_creation_quota") is not None
                else user.workspace_creation_quota
            )

        user.save()

        return HttpResponseGenerator.generate_response(HttpStatus.OK)
