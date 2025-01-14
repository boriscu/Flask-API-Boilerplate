import ast
from typing import Optional
from flask import abort

from app.models.enums.http_status import HttpStatus

from app.models.pg.user_profile import UserProfile
from app.models.pg.workspace_user import WorkspaceUser

from app.services.user_services.user_auth_service import UserAuthService
from app.services.workspace_user_services.workspace_user_access_control import (
    WorkspaceUserAccessControl,
)


class WorkspaceValidationService:
    @staticmethod
    def check_workspace_creation_quota(user_id: int):
        """
        Verifies whether a user has exceeded their allotted workspace creation quota.

        Args:
            user_id (int): The unique identifier of the user to check the workspace creation quota for.

        Raises:
            HTTPError: A 406 Not Acceptable error if the user's current workspace count exceeds or equals the quota.
        """

        user_profile = UserProfile.get_by_id(user_id)

        workspace_count = WorkspaceUserAccessControl.count_user_workspaces(
            user_profile.id
        )

        if (
            user_profile.workspace_creation_quota
            and workspace_count >= user_profile.workspace_creation_quota
        ):
            abort(HttpStatus.NOT_ACCEPTABLE.value)

    @staticmethod
    def get_parsed_admin_namespaces(raw_namespaces: Optional[str] = None):
        """
        Retrieves and parses namespaces based on user permissions. Only admin users can
        specify namespaces. Non-admins receive an empty list.

        If the user is an admin, the method checks if the provided  raw_namespaces is the '*' wildcard,
        in which case it returns '*', indicating all namespaces.
        Otherwise, it assumes the input is a string representation of a list of strings and attempts
        to parse it using ast.literal_eval.

        Parameters:
        - raw_namespaces (Optional[str]): A string representation of namespaces or a wildcard character '*',
        which can be None if not specified. Default is None.

        Returns:
        - Union[List[str], str, list]: A list of namespaces if the input is a valid list string,
        the '*' character if the input is '*', or an empty list if the user is not authorized to
        specify namespaces or if no namespaces are provided.

        Raises:
        - ValueError: If the input string is malformed and cannot be parsed into a list of strings.
        """
        if not UserAuthService.check_if_admin() or raw_namespaces == None:
            return []

        if raw_namespaces == "*":
            return "*"
        else:
            return ast.literal_eval(raw_namespaces)

    @staticmethod
    def count_workspace_users(workspace_id: int) -> int:
        """
        Counts the number of users that are part of a specified workspace.

        Args:
            workspace_id (int): The unique identifier of the workspace.

        Returns:
            int: The number of users associated with the workspace.
        """
        return (
            WorkspaceUser.select()
            .where(WorkspaceUser.workspace == workspace_id)
            .count()
        )
