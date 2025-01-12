from flask import abort
from peewee import fn

from app.models.enums.http_status import HttpStatus
from app.models.enums.workspace_user_role import WorkspaceUserRole

from app.models.pg.workspace_user import WorkspaceUser

from app.services.user_services.user_auth_service import UserAuthService


class WorkspaceUserAccessControl:
    @staticmethod
    def count_user_workspaces(user_id: int) -> int:
        """
        Counts the number of workspaces associated with a given user based on their user_id.

        Args:
        user_id (int): The unique identifier of the user whose workspaces are to be counted.

        Returns:
        int: The number of workspaces associated with the user. Returns None if the user does not exist or an error occurs.
        """
        return (
            WorkspaceUser.select(fn.COUNT(WorkspaceUser.workspace_id))
            .where(WorkspaceUser.user_id == user_id)
            .scalar()
        )

    @staticmethod
    def get_user_role(workspace_id: int, user_id: int) -> int:
        """
        Retrieves the role value of a user within a specific workspace.

        Args:
            workspace_id (int): The ID of the workspace.
            user_id (int): The ID of the user.

        Returns:
            Optional[int]: The role value of the user in the workspace if they have a role; otherwise, None.

        Notes:
            This method returns None if the workspace-user relationship does not exist.
        """
        try:
            workspace_user = WorkspaceUser.get(workspace=workspace_id, user=user_id)
            return WorkspaceUserRole(workspace_user.workspace_user_role).value
        except:
            return None

    @staticmethod
    def check_workspace_user_access(workspace_id: int, user_id: int) -> bool:
        """
        Checks if a user has access to a specific workspace by verifying the existence of a workspace-user relationship.

        Args:
            workspace_id (int): The ID of the workspace.
            user_id (int): The ID of the user.

        Returns:
            bool: True if the user has access to the workspace, False otherwise.

        """
        try:
            WorkspaceUser.get(workspace=workspace_id, user=user_id)
            return True
        except:
            return False

    @staticmethod
    def check_operation_access_rights(workspace_id: int, user_id: int):
        """
        Verifies if a user has administrative rights or specific access rights to a workspace. If the user does not have the necessary rights, the operation is aborted with an HTTP 403 Forbidden status.

        Args:
            workspace_id (int): The ID of the workspace for which access rights are being checked.
            user_id (int): The ID of the user whose access rights are being verified.

        Raises:
            HTTPException: Aborts the current request and raises an HTTP 403 Forbidden if the user does not have the required access rights.
        """

        if (
            not UserAuthService.check_if_admin()
            and not WorkspaceUserAccessControl.check_workspace_user_access(
                workspace_id, user_id
            )
        ):
            abort(HttpStatus.FORBIDDEN.value)
