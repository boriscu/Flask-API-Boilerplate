from peewee import ForeignKeyField, IntegerField

from app.models.enums.workspace_user_role import WorkspaceUserRole

from app.models.pg.base import BaseModel
from app.models.pg.user_profile import UserProfile
from app.models.pg.workspace import Workspace


class WorkspaceUser(BaseModel):
    workspace = ForeignKeyField(Workspace, null=False, on_delete="CASCADE")
    user = ForeignKeyField(UserProfile, null=False, on_delete="CASCADE")
    workspace_user_role = IntegerField(default=WorkspaceUserRole.VIEW.value)
