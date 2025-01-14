from typing import Any, Dict, Tuple
from flask import abort

from app.models.enums.http_status import HttpStatus
from app.models.enums.workspace_user_role import WorkspaceUserRole

from app.models.pg.workspace import Workspace
from app.services.workspace_services.workspace_validation_service import (
    WorkspaceValidationService,
)
from app.services.workspace_user_services.workspace_user_access_control import (
    WorkspaceUserAccessControl,
)


class WorkspaceUserInviteValidationService:
    @staticmethod
    def _validate_workspace_user_role(workspace_user_role: int) -> WorkspaceUserRole:
        """
        Validates the given workspace user role.

        Parameters:
        - workspace_user_role (int): The role ID of a user in the workspace.

        Returns:
        - WorkspaceUserRole: An enum value of the workspace user role.

        Raises:
        - HttpStatus.CONFLICT: If the role is 'ADMIN'.
        """
        workspace_user_role = WorkspaceUserRole(workspace_user_role)

        if workspace_user_role == WorkspaceUserRole.ADMIN:
            abort(HttpStatus.CONFLICT.value)

        return workspace_user_role

    @staticmethod
    def _check_invitor(invitor_id: int, workspace_id: int):
        """
        Checks if the invitor has admin rights in the workspace.

        Parameters:
        - invitor_id (int): The ID of the invitor.
        - workspace_id (int): The ID of the workspace.

        Raises:
        - HttpStatus.FORBIDDEN: If the invitor does not have admin rights.
        """
        if not WorkspaceUserAccessControl.check_workspace_user_access(
            workspace_id=workspace_id,
            user_id=invitor_id,
            required_role=WorkspaceUserRole.ADMIN,
        ):
            abort(HttpStatus.FORBIDDEN.value)

    @staticmethod
    def _check_invited(invited_id: int, workspace_id: int):
        """
        Checks if the invited user is already part of the workspace with any assigned role.

        Parameters:
        - invited_id (int): The ID of the invited user.
        - workspace_id (int): The ID of the workspace.

        Raises:
        - HttpStatus.BAD_REQUEST: If the invited user is already part of the workspace.
        """

        if WorkspaceUserAccessControl.check_workspace_user_access(
            workspace_id=workspace_id,
            user_id=invited_id,
            required_role=WorkspaceUserRole.VIEW,
        ):
            abort(HttpStatus.BAD_REQUEST.value)

    @staticmethod
    def _check_workspace_limit(workspace_id):
        """
        Checks if the workspace has reached its limit of users.

        Parameters:
        - workspace_id (int): The ID of the workspace.

        Raises:
        - HttpStatus.NOT_ACCEPTABLE: If the user limit for the workspace is reached.
        """
        workspace = Workspace.get_by_id(workspace_id)

        if (
            WorkspaceValidationService.count_workspace_users(workspace_id)
            >= workspace.user_limit
        ):
            abort(HttpStatus.NOT_ACCEPTABLE.value)

    @staticmethod
    def validate_invitation(
        workspace_id: int, invitor_id: int, data: Dict[str, Any]
    ) -> Tuple[int, WorkspaceUserRole]:
        """
        Validates an invitation based on workspace rules and roles.

        Parameters:
        - workspace_id (int): The ID of the workspace.
        - invitor_id (int): The ID of the invitor.
        - data (dict): Contains details of the invitation such as 'user_id' and 'workspace_user_role'.

        Returns:
        - Tuple[int, WorkspaceUserRole]: Returns the invited user's ID and role.

        Raises relevant HTTP status exceptions based on various checks.
        """
        invited_id = data.get("user_id")

        WorkspaceUserInviteValidationService._check_invitor(invitor_id, workspace_id)
        WorkspaceUserInviteValidationService._check_invited(invited_id, workspace_id)
        workspace_user_role = (
            WorkspaceUserInviteValidationService._validate_workspace_user_role(
                data.get("workspace_user_role", WorkspaceUserRole.VIEW.value)
            )
        )
        WorkspaceUserInviteValidationService._check_workspace_limit(workspace_id)
        return invited_id, workspace_user_role
