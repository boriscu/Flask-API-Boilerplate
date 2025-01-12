from flask import abort

from app.models.enums.http_status import HttpStatus
from app.models.pg.user_profile import UserProfile

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
