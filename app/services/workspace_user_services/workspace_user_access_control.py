from peewee import fn

from app.models.pg.workspace_user import WorkspaceUser


class UserWorkspaceAccessControl:
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
            WorkspaceUser.select(fn.COUNT(WorkspaceUser.workspace))
            .where(WorkspaceUser.user_id == user_id)
            .scalar()
        )
