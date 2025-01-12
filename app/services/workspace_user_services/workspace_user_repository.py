from app.models.enums.workspace_user_role import WorkspaceUserRole
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
