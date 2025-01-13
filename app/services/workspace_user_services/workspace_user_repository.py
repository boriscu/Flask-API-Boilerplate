from flask_jwt_extended import get_jwt_identity

from app.models.enums.workspace_type import WorkspaceType
from app.models.enums.workspace_user_role import WorkspaceUserRole

from app.models.pg.workspace import Workspace
from app.models.pg.workspace_user import WorkspaceUser


class WorkspaceUserRepository:
    @staticmethod
    def create_workspace_user_relation(user_id: int, workspace_id: int):
        """
        Adds a user to a workspace with an admin role.

        Args:
            user_id (int): The ID of the user to be added to the workspace.
            workspace_id (int): The ID of the workspace where the user will be added.

        """

        WorkspaceUser.create(
            user_id=user_id,
            workspace_id=workspace_id,
            workspace_user_role=WorkspaceUserRole.ADMIN.value,
        )

    @staticmethod
    def create_personal_workspace(user_name: str, user_id: int) -> Workspace:
        """
        Creates a new personal workspace for a specified user.

        Args:
            user_name (str): The name of the user for whom the workspace is being created.
            user_id (int): The unique identifier of the user.

        Returns:
            Workspace: An instance of the Workspace class representing the newly created personal workspace.

        """
        new_workspace = Workspace.create(
            name=f"{user_name}s' Workspace",
            description=f"Personal workspace for {user_name}",
            namespaces="[]",
            icon_image=None,
            workspace_type=WorkspaceType.PERSONAL.value,
        )

        WorkspaceUserRepository.create_workspace_user_relation(
            user_id, new_workspace.id
        )

        return new_workspace

    @staticmethod
    def get_personal_workspace() -> Workspace:
        """
        Retrieve the personal workspace associated with the current user.

        Returns:
            A Workspace instance representing the user's personal workspace
            or None if no personal workspace is found.
        """

        return (
            WorkspaceUser.select()
            .join(Workspace)
            .where(
                (WorkspaceUser.user == int(get_jwt_identity()))
                & (Workspace.workspace_type == WorkspaceType.PERSONAL.value)
            )
            .get()
        ).workspace
